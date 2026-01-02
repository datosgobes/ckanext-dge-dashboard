# Copyright (C) 2025 Entidad Pública Empresarial Red.es
#
# This file is part of "dge-dashboard (datos.gob.es)".
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

import csv
import datetime
import json
import logging
import urllib.request, urllib.parse, urllib.error
from datetime import datetime

import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.model as model
import ckanext.dge_dashboard.helpers as ddh
import ckantoolkit as tk
from ckan.common import c, _
import ckan.lib.base as base
from ckan.lib.base import render
from ckan.plugins import toolkit
from ckan.plugins.toolkit import config

from flask import Blueprint, send_file

log = logging.getLogger(__name__)
global_special_org_id = ""
backend = config.get('ckanext.dge_dashboard.chart.filepath')

dgeDashboard = Blueprint(
    'dgeDashboard',
    __name__,
)


def _write_error_csv(filename=datetime.now().strftime("%Y-%m-%d")):
    global backend
    path = backend + filename
    file = open(path, 'w')
    writer = csv.writer(file)
    writer.writerow([_('Error loading data')])
    file.close()


def __create_absolute_link(prefix, path):
    url = path.lstrip('/')
    p_url = urllib.parse.urlparse(url)
    if not (p_url.scheme or p_url.netloc):
        url = prefix.rstrip('/') + '/' + url
    return url


def dashboard():
    return render('dashboard/dashboard.html')


def my_dashboard():
    user = c.user
    org_id = None
    orgs = toolkit.get_action('organization_list_for_user')(data_dict={'permission': 'read'})
    if orgs and len(orgs) > 0:
        org_id = orgs[0].get('id', None) if orgs[0] else None
    aux = org_id.encode('ascii', 'ignore')
    if c.userobj:
        if ((c.userobj.sysadmin == True) or (aux == global_special_org_id)):
            return render('my_dashboard/administrator_dashboard.html')
        else:
            return render('my_dashboard/organization_dashboard.html')
    else:
        base.abort(401, _('Not authorized to see this page'))


def org_datasets_csv():
    '''
    Returns a CSV with the number of views for each dataset and
    its resources downloads.
    '''
    global backend
    response_data = None
    aux_filename = "%s_datasets_%s.csv" % ('org', datetime.now().strftime("%Y-%m-%d"))
    filename_path = "/var/www/html/dashboard/data/"
    path = backend + aux_filename
    file = open(path, 'w')
    try:
        organization = ddh._dge_dashboard_user_organization()
        org_id = organization.get('id', None) if organization else None
        if org_id:
            filename = config.get('ckanext.dge_dashboard.chart.org.most_visited_datasets.csv_url_data.filename', None)
            filename = filename.format(org_id) if filename else None
            if filename:
                read_path = filename_path + filename if filename else None
                if read_path:
                    response_data = open(read_path, 'r')
                if response_data:
                    reader = csv.reader(response_data)
                    writer = csv.writer(file)
                    prefix_url = config.get(
                        'ckan.site_url') + h.url_for('package.search') + "/"
                    month_name_dict = {}
                    read_header = False
                    for row in reader:
                        if not read_header:
                            read_header = True
                            column_resources = '%s(%s)' % (_('Resource'), _('Downloads'))
                            writer.writerow([_('Month'), _('Url'), _('Dataset'), _('Public_Private'), _('Publisher'), _('Visits'), column_resources])
                        else:
                            month_name = month_name_dict.get(row[0], None)
                            if not month_name:
                                month_name = ddh.dge_dashboard_get_month(
                                    row[0], int(row[1]))
                                month_name_dict[row[0]] = month_name
                            dataset_title = row[3]
                            if row[2] == row[3]:
                                dataset_title = '[%s] %s' % (_('Deleted'), row[3])
                            dataset_public_private = ''
                            if row[4] is not None and row[4].lower() == 'true':
                                dataset_public_private = _('Private')
                            elif row[4] is not None and row[4].lower() == 'false':
                                dataset_public_private = _('Public')

                            writer.writerow([
                                month_name,
                                prefix_url + row[2],
                                dataset_title,
                                dataset_public_private,
                                row[5],
                                row[6],
                                row[7]
                            ])
            if not filename or not read_path or not response_data:
                _write_error_csv(aux_filename)
        else:
            base.abort(401, _('Not authorized to see this page'))
    except Exception as e:
        log.error('Exception in org_datasets_csv: %s', e)
        _write_error_csv(aux_filename)
    
    return send_file(path, as_attachment=True, attachment_filename=aux_filename)


def org_users_csv():
    '''
    Returns a CSV with the users of an organization.
    '''
    global backend
    filename = "%s_users_%s.csv" % (
        'org', datetime.now().strftime("%Y-%m-%d"))
    path = backend + filename
    file = open(path, 'w')
    try:
        json_result_data, json_column_titles, total, data_date, error_loading_data = ddh.dge_dashboard_organization_data_users()
        if error_loading_data:
            _write_error_csv(filename)
        else:
            result_data = json.loads(
                json_result_data) if json_result_data else []
            column_titles = [_('Updated date'), _('Username')]
            writer = csv.writer(file)
            writer.writerow(column_titles)
            for result in result_data:
                row = [
                    result.get('date', ''),
                    result.get('username', '')
                ]
                writer.writerow(row)
    except Exception as e:
        log.error('Exception in org_users_csv: %s', e)
        _write_error_csv(file)
    finally:
        if file: file.close()
    
    return send_file(path, as_attachment=True, attachment_filename=filename)      


def adm_drupal_contents_csv():
    '''
    Returns a CSV with the number of drupal contents by content type
    '''
    global backend
    filename = "contents_number_%s.csv" % (datetime.now().strftime("%Y-%m-%d"))
    path = backend + filename
    file = open(path, 'w')
    try:
        json_result_data, json_column_titles, total, data_date, error_loading_data = ddh.dge_dashboard_administrator_published_drupal_contents()
        if error_loading_data:
            _write_error_csv(path)
        else:
            result_data = json.loads(json_result_data) if json_result_data else []
            column_titles = [_('Updated date'), _('Content type'), _('Content number')]
            writer = csv.writer(file)
            writer.writerow(column_titles)
            for result in result_data:
                row = [
                    result.get('date', ''),
                    result.get('content_type', ''),
                    result.get('num_contents', 0)
                ]
                writer.writerow(row)
    except Exception as e:
        log.error('Exception in adm_drupal_contents_csv: %s', e)
        _write_error_csv(file)
    finally:
        if file: file.close()

    return send_file(path, as_attachment=True, attachment_filename=filename)


def adm_users_by_org_csv():
    '''
    Returns a CSV with the number of users by organizationn
    '''
    global backend
    filename = "users_organization_%s.csv" % (datetime.now().strftime("%Y-%m-%d"))
    path = backend + filename
    file = open(path, 'w')
    try:
        json_result_data, json_column_titles, total, data_date, error_loading_data = ddh.dge_dashboard_administrator_data_users()
        if error_loading_data:
            _write_error_csv(path)
        else:
            result_data = json.loads(json_result_data) if json_result_data else []
            column_titles = [_('Updated date'), _('Organization name'), _('Users number')]
            writer = csv.writer(file)
            writer.writerow(column_titles)
            for result in result_data:
                row = [
                    result.get('date', ''),
                    result.get('organization', ''),
                    result.get('num_users', 0)
                ]
                writer.writerow(row)

    except Exception as e:
        log.error('Exception in adm_users_by_org_csv: %s', e)
        _write_error_csv(file)

    finally:
        if file: file.close()

    return send_file(path, as_attachment=True, attachment_filename=filename)


def adm_datasets_by_res_csv():
    '''
    Returns a CSV with the number of datasets by resoucers number
    '''
    global backend
    filename = "datasets_resources_%s.csv" % (datetime.now().strftime("%Y-%m-%d"))
    path = backend + filename
    file = open(path, 'w')
    try:
        json_result_data, json_month_name_list, month_name_list, json_column_titles, error_loading_data = ddh.dge_dashboard_administrator_data_num_datasets_by_num_resources()
        if error_loading_data:
            _write_error_csv(path)
        else:
            result_data = json.loads(json_result_data) if json_result_data else []
            column_titles = [_('Month'), _('Resources Number'), _('Datasets Number')]
            writer = csv.writer(file)
            writer.writerow(column_titles)
            for result in result_data:
                row = [
                    result.get('month', ''),
                    result.get('num_resources', 0),
                    result.get('num_datasets', 0)
                ]
                writer.writerow(row)
    except Exception as e:
        log.error('Exception in adm_datasets_by_res_csv: %s', e)
        _write_error_csv(file)
    finally:
        if file: file.close()

    return send_file(path, as_attachment=True, attachment_filename=filename)


def most_visited_datasets_csv():
    '''
    Returns a CSV with the most_visited_datasets.
    '''
    global backend
    filename = "most_visited_datasets_%s.csv" % datetime.now().strftime("%Y-%m-%d")
    path = backend + filename
    file = open(path, 'w')
    try:
        json_result_data, json_month_name_list, month_name_list, json_column_titles, visible_visits = ddh.dge_dashboard_data_most_visited_datasets(
            True)
        visible_visits = tk.asbool(
            config.get('ckanext.dge_dashboard.chart.most_visited_datasets.num_visits.csv.visible', False))

        result_data = json.loads(json_result_data) if json_result_data else []
        column_titles = [_('Month'), _('Url'), _('Dataset'),
                         _('Publisher')]
        if visible_visits:
            column_titles.append(_('Visits'))
        writer = csv.writer(file)
        writer.writerow(column_titles)
        prefix_url = config.get('ckan.site_url') + h.url_for('package.search') + "/"
        for result in result_data:
            row = [
                result.get('month', ''),
                prefix_url + result.get('url', ''),
                result.get('title', ''),
                result.get('publisher', '')
            ]
            if visible_visits:
                row.append(result.get('visits', 0))
            writer.writerow(row)
    except Exception as e:
        log.error('Exception in most_visited_datasets_csv: %s', e)
        _write_error_csv(filename)
    finally:
        if file: file.close()

    return send_file(path, as_attachment=True, attachment_filename=filename)


def adm_datasets_by_org_csv():
    '''
    Returns a CSV with the number of users by organizationn
    '''

    # Checking if user is allowed to access to
    global backend
    user = c.user
    org_id = None
    orgs = toolkit.get_action('organization_list_for_user')(data_dict={'permission': 'read'})
    if orgs and len(orgs) > 0:
        org_id = orgs[0].get('id', None) if orgs[0] else None
    aux = org_id.encode('ascii', 'ignore')
    abort_request = False
    if c.userobj:
        if not ((c.userobj.sysadmin) or (aux == global_special_org_id)):
            abort_request = True
    else:
        abort_request = True

    if abort_request:
        base.abort(401, _('Not authorized to see this page'))
    filename = "datasets_by_organization_%s.csv" % (datetime.now().strftime("%Y-%m-%d"))
    path = backend + filename
    file = open(path, 'w')
    try:
        result_data, column_titles, error_loading_data = ddh.dge_dashboard_administrator_datasets_by_org()
        if error_loading_data:
            _write_error_csv(path)
        else:
            column_titles.insert(0, _('Organization name'))
            writer = csv.writer(file)
            writer.writerow(column_titles)
            # Remove additional header
            del column_titles[0]
            for result in result_data:
                row = []
                row.append(result.get('title', ''))
                # Get organization data
                org_data = result.get('data', {})
                for date in column_titles:
                    if date in org_data:
                        row.append(org_data[date])
                    else:
                        row.append(' ')
                writer.writerow(row)
    except Exception as e:
        log.error('Exception in adm_datasets_by_org_csv: %s', e)
        _write_error_csv(path)
    finally:
        if file: file.close()

    return send_file(path, as_attachment=True, attachment_filename=filename)


def adm_organizations_by_level():
    '''
    Returns a CSV with the organizations by level with the type of federation
    '''
    global backend
    filename = "orgs_by_level_%s.csv" % (datetime.now().strftime("%Y-%m-%d"))
    path = backend + filename
    file = open(path, 'w')
    try:
        json_result_data, json_column_titles, data_date, error_loading_data = ddh.dge_dashboard_administrator_organizations_by_level()
        if error_loading_data:
            _write_error_csv(path)
        else:
            result_data = json.loads(json_result_data) if json_result_data else []
            column_titles = [_('Updated date'), _('Organization'), _('Administration level'),
                             _('Type of actualization')]
            writer = csv.writer(file)
            writer.writerow(column_titles)
            for result in result_data:
                row = [
                    result.get('date', ''),
                    result.get('organization', ''),
                    result.get('category', ''),
                    result.get('type_actualization', '')
                ]
                writer.writerow(row)
    except Exception as e:
        log.error('Exception in adm_organizations_by_level: %s', e)
        _write_error_csv(filename)
    finally:
        if file: file.close()

    return send_file(path, as_attachment=True, attachment_filename=filename)


def adm_drupal_contents_by_likes_csv():
    global backend
    filename = "likes_%s.csv" % (datetime.now().strftime("%Y-%m-%d"))
    path = backend + filename
    file = open(path, 'w')
    try:
        likes_info, column_titles, error_loading_data = \
            ddh.dge_dashboard_administrator_drupal_contents_by_likes()
        if error_loading_data:
            _write_error_csv(path)
        else:
            rows = json.loads(likes_info['data'])
            writer = csv.writer(file)
            writer.writerow([col for col in json.loads(column_titles)])
            site_url = config.get('ckan.site_url')
            for row in rows:
                writer.writerow([
                    row.get('name', ''),
                    __create_absolute_link(site_url, row.get('url', '')),
                    int(row.get('likes', 0)),
                    row.get('content_type', '')
                ])
    except Exception as e:
        log.error('Exception in adm_drupal_contents_by_likes_csv: %s', e)
        _write_error_csv(file)
    finally:
        if file: file.close()

    return send_file(path, as_attachment=True, attachment_filename=filename)


def adm_drupal_contents_top10_voted_datasets_csv():
    global backend
    filename = "top10_voted_datasets_%s.csv" % (datetime.now().strftime("%Y-%m-%d"))
    path = backend + filename
    file = open(path, 'w')
    try:
        top10_info, column_titles, error_loading_data = \
            ddh.dge_dashboard_administrator_drupal_top10_voted_datasets()
        if error_loading_data:
            _write_error_csv(filename)
        else:
            rows = json.loads(top10_info['data'])
            writer = csv.writer(file)
            writer.writerow([col for col in json.loads(column_titles)])
            site_url = config.get('ckan.site_url')
            for row in rows:
                writer.writerow([
                    row.get('name', ''),
                    __create_absolute_link(site_url, row.get('url', '')),
                    int(row.get('likes', 0))
                ])
    except Exception as e:
        log.error('Exception in adm_drupal_contents_top10_voted_datasets_csv: %s', e)
        _write_error_csv(filename)
    finally:
        if file: file.close()

    return send_file(path, as_attachment=True, attachment_filename=filename)


dgeDashboard.add_url_rule('/dashboard', 'dashboard', view_func=dashboard)
dgeDashboard.add_url_rule('/my-dashboard', 'my_dashboard', view_func=my_dashboard)
dgeDashboard.add_url_rule('/csv-download/org-datasets', 'org_datasets_csv', view_func=org_datasets_csv)
dgeDashboard.add_url_rule('/csv-download/org-users', 'org_users_csv', view_func=org_users_csv)
dgeDashboard.add_url_rule('/csv-download/adm-drupal-contents', 'adm_drupal_contents_csv', view_func=adm_drupal_contents_csv)
dgeDashboard.add_url_rule('/csv-download/adm-users-org', 'adm_users_by_org_csv', view_func=adm_users_by_org_csv)
dgeDashboard.add_url_rule('/csv-download/adm-datasets-res', 'adm_datasets_by_res_csv', view_func=adm_datasets_by_res_csv)
dgeDashboard.add_url_rule('/csv-download/most-visited-datasets', 'most_visited_datasets_csv', view_func=most_visited_datasets_csv)
dgeDashboard.add_url_rule('/csv-download/adm-org-datasets', 'adm_datasets_by_org_csv', view_func=adm_datasets_by_org_csv)
dgeDashboard.add_url_rule('/csv-download/adm-organizations-by-level', 'adm_organizations_by_level', view_func=adm_organizations_by_level)
dgeDashboard.add_url_rule('/csv-download/adm_drupal_contents_by_likes', 'adm_drupal_contents_by_likes_csv', view_func=adm_drupal_contents_by_likes_csv)
dgeDashboard.add_url_rule('/csv-download/adm_drupal_contents_top10_voted_datasets', 'adm_drupal_contents_top10_voted_datasets_csv', view_func=adm_drupal_contents_top10_voted_datasets_csv)