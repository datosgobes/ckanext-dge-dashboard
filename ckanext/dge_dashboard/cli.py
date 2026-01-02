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

from __future__ import print_function

import click
import re
import sys

from datetime import datetime
from ckan import model
import ckan.plugins.toolkit as tk

PUBLISHED_DATASETS_TYPES = ['total', 'all', 'adm_level', 'org', 'num_res']
DISTRIBUTION_FORMAT_TYPES = ['total', 'adm_level', 'org']
DRUPAL_PUBLISHED_CONTENTS = ['contents', 'comments', 'org_comments']
USERS_TYPES = ['org', 'adm_level', 'num_org']
REQUEST_TYPES = ['total', 'org']
VISIT_TYPES = ['total', 'section']
COMMENTS_TYPES = ['total', 'org']
VISITED_DATASET_TYPES = ['total', 'org']

FILENAME_REGEX = '^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$'

def get_commands():
    return [dge_dashboard_init_db,dge_dashboard_load,dge_dashboard_json,dge_dashboard_csv]

def _set_context():
    context = {'model':model,'session':model.Session,'ignore_auth':True}
    admin_user = tk.get_action('get_site_user')(context, {})
    return {
        'model': model,
        'session': model.Session,
        'user': admin_user['name'],
        'ignore_auth': True,
    }

@click.group("dge_dashboard_init_db")
def dge_dashboard_init_db():
    '''Usage:
    dge_dashboard_init_db initdb [paster --plugin=ckanext-dge-dashboard dge_dashboard_init_db initdb -c /etc/ckan/default/production.ini]
        - Creates the necessary tables in the database and complete them with historical data
    '''
    pass

@dge_dashboard_init_db.command()
def initdb():
    from ckanext.dge_dashboard.model import setup as db_setup
    db_setup()
    click.echo('DB tables created')

@click.group("dge_dashboard_load")
def dge_dashboard_load():
    ''' Save data to the database dga_dashboard tables
    Usage:

    dge_dashboard_load published_datasets [paster --plugin=ckanext-dge-dashboard dge_dashboard_load published_datasets {save|print} {latest|YYYY-MM|last_month} -c /etc/ckan/default/production.ini]
        - Updates dge_dashboard_published_datasets table with public and active datasets created until and during the given month. Params:
          - {save|print}: save if save data in database; print if only print data, not save in database
          - {lastest|YYYY-MM|last_month}: just data for...
                 actual month if None
                 specific month if YYYY-MM
                 last month if last_month


    dge_dashboard_load published_datasets_by_num_resources [paster --plugin=ckanext-dge-dashboard dge_dashboard_load published_datasets_by_num_resources {save|print} {latest|YYYY-MM|last_month} -c /etc/ckan/default/production.ini]
        - Updates update_published_datasets_by_num_resources table with public and active datasets created until and during the given month. Params
          - {save|print}: save if save data in database; print if only print data, not save in database
          - {latest|YYYY-MM|last_month}: just data for...
                 actual month if None
                 specific month if YYYY-MM
                 last month if last_month


    dge_dashboard_load publishers [paster --plugin=ckanext-dge-dashboard dge_dashboard_load publishers {save|print} {latest|YYYY-MM|last_month} -c /etc/ckan/default/production.ini]
        - Updates dge_dashboard_publishers table with num harvester publishers and manual loadings publishers than
          have published datasets until and during the given month. Params:
          - {latest|save|print}: save if save data in database; print if only print data, not save in database
          - {latest|YYYY-MM|last_month}: just data for...
                 actual month if None
                 specific month if YYYY-MM
                 last month if last_month


    dge_dashboard_load drupal_published_contents [paster --plugin=ckanext-dge-dashboard dge_dashboard_load drupal_published_contents {save|print} {latest|YYYY-MM|last_month} -c /etc/ckan/default/production.ini]
        - Updates update_drupal_published_contents table with drupal contents created until and during the given month. Params:
          - {save|print}: save if save data in database; print if only print data, not save in database
          - {latest|YYYY-MM|last_month}: just data for...
                 actual month if None
                 specific month if YYYY-MM
                 last month if last_month


    dge_dashboard_load drupal_comments [paster --plugin=ckanext-dge-dashboard dge_dashboard_load drupal_comments {save|print} {latest|YYYY-MM|last_month} -c /etc/ckan/default/production.ini]
        - Updates update_drupal_published_contents table with drupal comments created until and during the given month. Params:
          - {save|print}: save if save data in database; print if only print data, not save in database
          - {latest|YYYY-MM|last_month}: 
                latest      - (default) just data for the current month
                YYYY-MM     - just data for the specific month
                last_month  - just data for the last month
          
    '''
    pass

def _validate_args(dtype, time_period, method_log_prefix=''):
    for_date = None
    save = False
    if dtype != 'save' and dtype != 'print':
        click.secho('{0} Please provide a valid type (save or print)'.format(method_log_prefix))
        sys.exit()
    else:
        if dtype == 'save':
            save = True

    if time_period == 'latest':
        time_period = datetime.now().strftime("%Y-%m")
    elif time_period == 'last_month':
        now = datetime.now()
        if now.month == 1:
            last_month = datetime(now.year - 1, 12, 1, 0, 0, 0)
        else:
            last_month = datetime(now.year, now.month - 1, 1, 0, 0, 0)
        time_period = last_month.strftime("%Y-%m")

    try:
        for_date = datetime.strptime(time_period, '%Y-%m')
    except ValueError as e:
        click.secho('{0} Please provide a valid second param (latest|YYYY-MM|last_month)'.format(method_log_prefix))
        sys.exit(1)

    if for_date:
        year = for_date.year
        month = for_date.month
    if month == 12:
        calculation_date = datetime(year + 1, 1, 1, 0, 0, 0)
    else:
        calculation_date = datetime(year, month + 1, 1, 0, 0, 0)
    return save, time_period, calculation_date

@dge_dashboard_load.command("published_datasets")
@click.argument(u"dtype")
@click.argument(u"time_period")
@click.pass_context
def published_datasets(ctx, dtype, time_period, num_resources=False):

    method_log_prefix = '[CliDgeDashboardLoad][published_datasets]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
    
        save, time_period, calculation_date = _validate_args(dtype,time_period,method_log_prefix) 
        tk.get_action('dge_dashboard_update_published_datasets')(context, {'date': str(calculation_date),
                                                                        'import_date': time_period,
                                                                        'num_resources': num_resources, 'save': save})
        if save:
            click.secho('Updated dge_dashboard_published_datasets table with data of {0}'.format(time_period))
    
    click.secho('{0} End method.'.format(method_log_prefix))
    sys.exit(0)

@dge_dashboard_load.command("published_datasets_by_num_resources")
@click.argument(u"dtype")
@click.argument(u"time_period")
@click.pass_context
def published_datasets_by_num_resources(ctx, dtype, time_period, num_resources=True):
    method_log_prefix = '[CliDgeDashboardLoad][published_datasets_by_num_resources]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        save, time_period, calculation_date = _validate_args(dtype,time_period,method_log_prefix)
        tk.get_action('dge_dashboard_update_published_datasets')(context, {'date': str(calculation_date),
                                                                        'import_date': time_period,
                                                                        'num_resources': num_resources, 'save': save})
        if save:
            click.secho('Updated dge_dashboard_published_datasets table with data of {0}'.format(time_period))
    click.secho('{0} End method.'.format(method_log_prefix))
    sys.exit(0)

@dge_dashboard_load.command("publishers")
@click.argument(u"dtype")
@click.argument(u"time_period")
@click.pass_context
def publishers(ctx, dtype, time_period):
    method_log_prefix = '[CliDgeDashboardLoad][publishers]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        save, time_period, calculation_date = _validate_args(dtype,time_period,method_log_prefix)
        tk.get_action('dge_dashboard_update_publishers')(context,
                                                        {'date': str(calculation_date), 'import_date': time_period,
                                                        'save': save})
        if save:
            click.secho('Updated dge_dashboard_publishers table with data of {0}'.format(time_period))

    click.secho('{0} End method.'.format(method_log_prefix))

@dge_dashboard_load.command("drupal_published_contents")
@click.argument(u"dtype")
@click.argument(u"time_period")
@click.pass_context
def drupal_published_contents(ctx, dtype, time_period, num_resources=False):
    method_log_prefix = '[CliDgeDashboardLoad][drupal_published_contents]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        save, time_period, calculation_date = _validate_args(dtype,time_period,method_log_prefix)
        tk.get_action('dge_dashboard_update_drupal_published_contents')(context,
                                                                        {'date': calculation_date.strftime("%Y/%m/%d"),
                                                                        'import_date': time_period, 'save': save})
        if save:
            click.secho('Updated dge_dashboard_update_drupal_published_contents table with data of {0}'.format(time_period))
    click.secho('{0} End method.'.format(method_log_prefix))

@dge_dashboard_load.command("drupal_comments")
@click.argument(u"dtype")
@click.argument(u"time_period")
@click.pass_context
def drupal_comments(ctx, dtype, time_period):
    method_log_prefix = '[CliDgeDashboardLoad][drupal_comments]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        save, time_period, calculation_date = _validate_args(dtype,time_period,method_log_prefix)
        tk.get_action('dge_dashboard_update_drupal_comments')(context, {'date': calculation_date.strftime("%Y/%m/%d"),
                                                                    'import_date': time_period, 'save': save})
        if save:
            click.secho('Updated dge_dashboard_drupal_contents table with data of {0}'.format(time_period))
    click.secho('{0} End method.'.format(method_log_prefix))

@click.group("dge_dashboard_json")
def dge_dashboard_json():
    ''' Command that generates json from the database files tables data 
    Usage:

    dge_dashboard_json published_datasets [paster --plugin=ckanext-dge-dashboard dge_dashboard_json published_datasets total|all|org|adm_level|num_res {destination} {prefix} -c /etc/ckan/default/production.ini]
        - Write json files with dge_dashboard_published_datasets table data. Params:
          - total|all|org|adm_level|num_res: If total, only total data; 
                                             if all, all data; 
                                             if org, organizations data;
                                             if adm_level, administration_level data;
                                             if num_res, num_resources;
          - {destination}: Destination directory of files
          - {prefix}: Prefix of filename. The filename will be {prefix}_{value of param1}.json

    dge_dashboard_json current_published_datasets_by_administration_level [paster --plugin=ckanext-dge-dashboard dge_dashboard_json current_published_datasets_by_administration_level {destination} {filename} -c /etc/ckan/default/production.ini]
        Write a json file with number of published datasets by administration level at this moment. Params:
         - {destination}: Destination directory of files
         - {filename}: The complete filename will be {filename}.json

    dge_dashboard_json current_distribution_format [paster --plugin=ckanext-dge-dashboard dge_dashboard_json current_distribution_format {[total|adm_level]} {destination} {filename} -c /etc/ckan/default/production.ini]
        Write a json file with number of distribution format global and by administration level at this moment. Params:
         - {total|adm_level|org}: total if total values, adm_level if values by administration level, org if values by organization
         - {destination}: Destination directory of files
         - {prefix}: Prefix of filename. The filename will be {prefix}_{value of param1}.json

    dge_dashboard_json current_published_datasets_by_category [paster --plugin=ckanext-dge-dashboard dge_dashboard_json current_published_datasets_by_category {destination} {filename} -c /etc/ckan/default/production.ini]
        Write a json file with number of published datasets by category at this moment. Params:
         - {destination}: Destination directory of files
         - {filename}: The complete filename will be {filename}.json

    dge_dashboard_json publishers [paster --plugin=ckanext-dge-dashboard dge_dashboard_json publishers {destination} {prefix} -c /etc/ckan/default/production.ini]
        - Write json files with dge_dashboard_publishers table data. Params:
          - {destination}: Destination directory of files
          - {filename}: The complete filename will be {filename}.json

    dge_dashboard_json current_publishers_by_administration_level [paster --plugin=ckanext-dge-dashboard dge_dashboard_json current_publishers_by_administration_level {destination} {prefix} -c /etc/ckan/default/production.ini]
        - Write json files with dge_dashboard_publishers by administration level in two groups, harvester publishers and manual loading publishers. Params:
          - {destination}: Destination directory of files
          - {filename}: The complete filename will be {filename}.json

    dge_dashboard_json drupal_published_datasets [paster --plugin=ckanext-dge-dashboard dge_dashboard_json drupal_published_content {total|org} {comments|no_comments} {destination} {prefix} -c /etc/ckan/default/production.ini]
        - Write json files with dge_dashboard_published_datasets table data. Params:
          - contents|comments|org_comments: If contents, only total data of app, intitatives, requests and success type contents; 
                                            if comments, total comments;
                                            if org_comments, organization comments;
          - {destination}: Destination directory of files
          - {prefix}: Prefix of filename. The filename will be {prefix}_{value of param1}.json

    dge_dashboard_json current_drupal_published_contents [paster --plugin=ckanext-dge-dashboard dge_dashboard_json current_drupal_published_contents {destination} {filename} -c /etc/ckan/default/production.ini]
        - Write json files with num of drupal published contents by content type. Params:
          - {destination}: Destination directory of files
          - {filename}: The complete filename will be {filename}.json

    dge_dashboard_json current_users [paster --plugin=ckanext-dge-dashboard dge_dashboard_json current_users_by_org {org|adm_level} {destination} {prefix} -c /etc/ckan/default/production.ini]
        - Write json files with active users .Params:
          - {org|adm_level|num_org}: org if active users users by organization plus usernames;
                                     num_org if number of active users by organization
                                     adm_level if active users by administration level;
          - {destination}: Destination directory of files
          - {filename}: The complete filename will be {filename}.json

    dge_dashboard_json current_assigned_request_by_state [paster --plugin=ckanext-dge-dashboard dge_dashboard_json current_assigned_request_by_state {total|org} {destination} {prefix} -c /etc/ckan/default/production.ini]
        Write a json file with number of assigned request by state at this moment. Params:
         - {total|org}: total if total values, org if values by organization
         - {destination}: Destination directory of files
         - {prefix}: Prefix of filename. The filename will be {prefix}_{value of param2}.json

    dge_dashboard_json visits [paster --plugin=ckanext-dge-dashboard dge_dashboard_json visits {destination} {filename} -c /etc/ckan/default/production.ini]
        - Write json files with visits to datos.gob.es. Params:
          - {destination}: Destination directory of files
          - {filename}: The complete filename will be {filename}.json

    dge_dashboard_json visits_by_section [paster --plugin=ckanext-dge-dashboard dge_dashboard_json visits_by_section {destination} {filename} -c /etc/ckan/default/production.ini]
        - Write json files with visits to datos.gob.es. Params:
          - {destination}: Destination directory of files
          - {filename}: The complete filename will be {filename}.json

    dge_dashboard_json visits [paster --plugin=ckanext-dge-dashboard dge_dashboard_json visits {total|section} {destination} {prefix} -c /etc/ckan/default/production.ini]
        Write a json file with number of visits to portal totals or by sections. Params:
         - {total|section}: total if total values, section if values by section
         - {destination}: Destination directory of files
         - {prefix}: Prefix of filename. The filename will be {prefix}_{value of param1}.json

    dge_dashboard_json visited_datasets [paster --plugin=ckanext-dge-dashboard dge_dashboard_json visited_datasets {total|org} {destination} {prefix} -c /etc/ckan/default/production.ini]
        Write a json file with the most visited datasets. Params:
         - {total|org}: total if total values, org if values by organization
         - {destination}: Destination directory of files
         - {prefix}: Prefix of filename. The filename will be {prefix}_{value of param1}.json

    dge_dashboard_json organization_by_administration_level [paster --plugin=ckanext-dge-dashboard dge_dashboard_json organization_by_administration_level {destination} {filename} -c /etc/ckan/default/production.ini]
        Write a json file with the most visited datasets. Params:
         - {destination}: Destination directory of files
         - {filename}: The complete filename will be {filename}.json
         
    dge_dashboard_json dge_dashboard_json_organization_name [paster --plugin=ckanext-dge-dashboard dge_dashboard_json organization_name {destination} {filename} -c /etc/ckan/default/production.ini]
        Write a json file with the most visited datasets. Params:
         - {destination}: Destination directory of files
         - {filename}: The complete filename will be {filename}.json

    '''
    pass

def _validate_destination_filename(destination, filename, is_prefix=False, method_log_prefix=''):
    if destination is None or len(destination) == 0 or len(destination.strip(' \t\n\r')) == 0:
        click.secho('{0} Please provide a destination'.format(method_log_prefix))
        sys.exit(1)
    else:
        destination = destination.strip(' \t\n\r')
    name = 'destination' if is_prefix else 'prefix'
    if filename is None or len(filename) == 0 or len(filename.strip(' \t\n\r')) == 0:
        click.secho('{0} Please provide a {1}'.format(method_log_prefix, name))
        sys.exit(1)
    else:
        filename = filename.strip(' \t\n\r')
        pattern = re.compile(FILENAME_REGEX)
        if not pattern.match(filename):
            click.secho('{0} Please provide a valid {1}. Regular expression: {2}'.format(method_log_prefix, name, filename_regex))
    return destination, filename


@dge_dashboard_json.command("published_datasets")
@click.argument(u"dtype")
@click.argument(u"destination")
@click.argument(u"prefix")
@click.pass_context
def published_datasets(ctx, dtype, destination, prefix):
    method_log_prefix = '[CliDgeDashboardJson][published_datasets]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        types = PUBLISHED_DATASETS_TYPES

        if dtype not in types:
            click.secho('{0} Please provide a valid type {1}'.format(method_log_prefix, types))
            sys.exit()
        destination, prefix = _validate_destination_filename(destination, prefix, True, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_published_datasets')(context, {'what': dtype,
                                                                                    'destination': destination,
                                                                                    'prefix': prefix})
        if outfilename:
            click.secho('Writed json with {0} data in {1}'.format(dtype, outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("current_published_datasets_by_administration_level")
@click.argument(u"destination")
@click.argument(u"filename")
@click.pass_context
def current_published_datasets_by_administration_level(ctx, destination, filename):
    method_log_prefix = '[CliDgeDashboardJson][current_published_datasets_by_administration_level]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        
        destination, filename = _validate_destination_filename(destination, filename, False, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_current_published_datasets_by_administration_level')(context, {
            'destination': destination, 'filename': filename})
        if outfilename:
            click.secho('Writed json in {0}'.format(outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("current_distribution_format")
@click.argument(u"dtype")
@click.argument(u"destination")
@click.argument(u"prefix")
@click.pass_context
def current_distribution_format(ctx, dtype, destination, prefix):
    method_log_prefix = '[CliDgeDashboardJson][current_distribution_format]'
    click.secho('{0} Init method.'.format(method_log_prefix))
    
    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        types = DISTRIBUTION_FORMAT_TYPES

        if dtype not in types:
            click.secho('{0} Please provide a valid type {1}'.format(method_log_prefix, types))
            sys.exit()
        destination, prefix = _validate_destination_filename(destination, prefix, True, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_current_distribution_format')(context, {'what': dtype,
                                                                                                'destination': destination,
                                                                                                'prefix': prefix})
        if outfilename:
            click.secho('Writed json with {0} data in {1}'.format(dtype, outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("current_published_datasets_by_category")
@click.argument(u"destination")
@click.argument(u"filename")
@click.pass_context
def current_published_datasets_by_category(ctx, destination, filename):
    method_log_prefix = '[CliDgeDashboardJson][current_published_datasets_by_category]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        
        destination, filename = _validate_destination_filename(destination, filename, False, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_current_published_datasets_by_category')(context, {
            'destination': destination, 'filename': filename})
        if outfilename:
            click.secho('Writed json in {0}'.format(outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("publishers")
@click.argument(u"destination")
@click.argument(u"filename")
@click.pass_context
def publishers(ctx, destination, filename):
    method_log_prefix = '[CliDgeDashboardJson][publishers]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        
        destination, filename = _validate_destination_filename(destination, filename, False, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_publishers')(context, {'destination': destination,
                                                                            'filename': filename})
        if outfilename:
            click.secho('Writed json in {0}'.format(outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("current_publishers_by_administration_level")
@click.argument(u"destination")
@click.argument(u"filename")
@click.pass_context
def current_publishers_by_administration_level(ctx, destination, filename):
    method_log_prefix = '[CliDgeDashboardJson][current_publishers_by_administration_level]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        
        destination, filename = _validate_destination_filename(destination, filename, False, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_current_publishers_by_administration_level')(context, {
            'destination': destination, 'filename': filename})
        if outfilename:
            click.secho('Writed json in {0}'.format(outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("drupal_published_contents")
@click.argument(u"dtype")
@click.argument(u"destination")
@click.argument(u"prefix")
@click.pass_context
def drupal_published_contents(ctx, dtype, destination, prefix):
    method_log_prefix = '[CliDgeDashboardJson][drupal_published_contents]'
    click.secho('{0} Init method.'.format(method_log_prefix))
    
    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        types = DRUPAL_PUBLISHED_CONTENTS

        if dtype not in types:
            click.secho('{0} Please provide a valid type {1}'.format(method_log_prefix, types))
            sys.exit()
        destination, prefix = _validate_destination_filename(destination, prefix, True, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_drupal_published_contents')(context, {'what': dtype,
                                                                                            'destination': destination,
                                                                                            'prefix': prefix})
        if outfilename:
            click.secho('Writed json with {0} data in {1}'.format(dtype, outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("current_drupal_published_contents")
@click.argument(u"destination")
@click.argument(u"filename")
@click.pass_context
def current_drupal_published_contents(ctx, destination, filename):
    method_log_prefix = '[CliDgeDashboardJson][current_drupal_published_contents]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        
        destination, filename = _validate_destination_filename(destination, filename, False, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_current_drupal_published_contents')(context, {
            'destination': destination, 'filename': filename})
        if outfilename:
            click.secho('Writed json in {0}'.format(outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("current_users")
@click.argument(u"dtype")
@click.argument(u"destination")
@click.argument(u"prefix")
@click.pass_context
def current_users(ctx, dtype, destination, prefix):
    method_log_prefix = '[CliDgeDashboardJson][current_users]'
    click.secho('{0} Init method.'.format(method_log_prefix))
    
    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        types = USERS_TYPES

        if dtype not in types:
            click.secho('{0} Please provide a valid type {1}'.format(method_log_prefix, types))
            sys.exit()
        destination, prefix = _validate_destination_filename(destination, prefix, True, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_current_users')(context, {'what': dtype, 'destination': destination,
                                                                          'prefix': prefix})
        if outfilename:
            click.secho('Writed json with {0} data in {1}'.format(dtype, outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("current_assigned_request_by_state")
@click.argument(u"dtype")
@click.argument(u"destination")
@click.argument(u"prefix")
@click.pass_context
def current_assigned_request_by_state(ctx, dtype, destination, prefix):
    method_log_prefix = '[CliDgeDashboardJson][current_assigned_request_by_state]'
    click.secho('{0} Init method.'.format(method_log_prefix))
    
    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        types = REQUEST_TYPES

        if dtype not in types:
            click.secho('{0} Please provide a valid type {1}'.format(method_log_prefix, types))
            sys.exit()
        destination, prefix = _validate_destination_filename(destination, prefix, True, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_current_assigned_request_by_state')(context, {'what': dtype,
                                                                                                       'destination': destination,
                                                                                                       'prefix': prefix})
        if outfilename:
            click.secho('Writed json with {0} data in {1}'.format(dtype, outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("visits")
@click.argument(u"dtype")
@click.argument(u"destination")
@click.argument(u"prefix")
@click.pass_context
def visits(ctx, dtype, destination, prefix):
    method_log_prefix = '[CliDgeDashboardJson][visits]'
    click.secho('{0} Init method.'.format(method_log_prefix))
    
    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        types = VISIT_TYPES

        if dtype not in types:
            click.secho('{0} Please provide a valid type {1}'.format(method_log_prefix, types))
            sys.exit()
        destination, prefix = _validate_destination_filename(destination, prefix, True, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_visits')(context, {'what': dtype, 'destination': destination,
                                                                            'prefix': prefix})
        if outfilename:
            click.secho('Writed json with {0} data in {1}'.format(dtype, outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("visited_datasets")
@click.argument(u"dtype")
@click.argument(u"destination")
@click.argument(u"prefix")
@click.pass_context
def visited_datasets(ctx, dtype, destination, prefix):
    method_log_prefix = '[CliDgeDashboardJson][visited_datasets]'
    click.secho('{0} Init method.'.format(method_log_prefix))
    
    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        types = VISITED_DATASET_TYPES

        if dtype not in types:
            click.secho('{0} Please provide a valid type {1}'.format(method_log_prefix, types))
            sys.exit()
        destination, prefix = _validate_destination_filename(destination, prefix, True, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_visited_datasets')(context,
                                                                            {'what': dtype, 'destination': destination,
                                                                             'prefix': prefix})
        if outfilename:
            click.secho('Writed json with {0} data in {1}'.format(dtype, outfilename))
        else:
            click.echo('No file was created')
        
        click.echo('Writing csv files...')
        tk.get_action('dge_dashboard_csv_visited_datasets')(context,
                                                                {'what': dtype, 'destination': destination,
                                                                 'prefix': prefix})
        click.echo('Writed csv files')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("organization_by_administration_level")
@click.argument(u"destination")
@click.argument(u"filename")
@click.pass_context
def organization_by_administration_level(ctx, destination, filename):
    method_log_prefix = '[CliDgeDashboardJson][organization_by_administration_level]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        
        destination, filename = _validate_destination_filename(destination, filename, False, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_organization_by_administration_level')(context, {
            'destination': destination, 'filename': filename})
        if outfilename:
            click.secho('Writed json in {0}'.format(outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("organization_name")
@click.argument(u"destination")
@click.argument(u"filename")
@click.pass_context
def organization_name(ctx, destination, filename):
    method_log_prefix = '[CliDgeDashboardJson][organization_name]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        
        destination, filename = _validate_destination_filename(destination, filename, False, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_organization_name')(context, {
            'destination': destination, 'filename': filename})
        if outfilename:
            click.secho('Writed json in {0}'.format(outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("content_by_likes")
@click.argument(u"destination")
@click.argument(u"filename")
@click.pass_context
def content_by_likes(ctx, destination, filename):
    method_log_prefix = '[CliDgeDashboardJson][current_drupal_content_by_likes]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        
        destination, filename = _validate_destination_filename(destination, filename, False, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_drupal_content_by_likes')(context, {
            'destination': destination, 'filename': filename})
        if outfilename:
            click.secho('Writed json in {0}'.format(outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))

@dge_dashboard_json.command("top10_voted_dataset")
@click.argument(u"destination")
@click.argument(u"filename")
@click.pass_context
def top10_voted_dataset(ctx, destination, filename):
    method_log_prefix = '[CliDgeDashboardJson][current_drupal_top10_voted_datasets]'
    click.secho('{0} Init method.'.format(method_log_prefix))

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()
        
        destination, filename = _validate_destination_filename(destination, filename, False, method_log_prefix)
        outfilename = tk.get_action('dge_dashboard_json_drupal_top10_voted_datasets')(context, {
            'destination': destination, 'filename': filename})
        if outfilename:
            click.secho('Writed json in {0}'.format(outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))


@click.group("dge_dashboard_csv")
def dge_dashboard_csv():
    ''' Command that generates csv from the database files tables data 
    Usage:
      dge_dashboard_csv published_datasets_by_root_org [paster --plugin=ckanext-dge-dashboard dge_dashboard_csv published_datasets_by_root_org {save|print} {YYYY-MM|last_month|latest} {destination} {filename} -c /etc/ckan/default/production.ini]
          - {save|print}: save if save data in file; print if only print data, not save in file
          - {latest|YYYY-MM|last_month}: 
                latest      - (default) just data for the current month
                YYYY-MM     - just data for the specific month
                last_month  - just data for the last month
          - {destination}: Destination directory of files
          - {filename}: The complete filename will be {filename}.json

  
    '''
    pass

def _validate_time_period(method_log_prefix='', time_period=None):
    for_date = None
    if time_period:
        if time_period == 'latest':
            time_period = datetime.now().strftime("%Y-%m")
        elif time_period == 'last_month':
            now = datetime.now()
            if now.month == 1:
                last_month = datetime(now.year - 1, 12, 1, 0, 0, 0)
            else:
                last_month = datetime(now.year, now.month - 1, 1, 0, 0, 0)
            time_period = last_month.strftime("%Y-%m")

        try:
            for_date = datetime.strptime(time_period, '%Y-%m')
        except ValueError as e:
            click.secho('{0} Please provide a valid second param (latest|YYYY-MM|last_month)'.format(method_log_prefix))
            sys.exit(1)

        if for_date:
            year = for_date.year
            month = for_date.month
        if month == 12:
            calculation_date = datetime(year + 1, 1, 1, 0, 0, 0)
        else:
            calculation_date = datetime(year, month + 1, 1, 0, 0, 0)
        return time_period, calculation_date
    else:
        click.secho('{0} Please provide valid params {print|save} {latest|YYYY-MM|last_month}'.format(method_log_prefix))
        sys.exit(1)

@dge_dashboard_csv.command("published_datasets_by_root_org")
@click.argument(u"dtype")
@click.argument(u"time_period", required=False)
@click.argument(u"destination")
@click.argument(u"filename")
@click.pass_context
def published_datasets_by_root_org(ctx, dtype, time_period, destination, filename):
    method_log_prefix = '[CliDgeDashboardCsv][published_datasets_by_root_org]'
    click.secho('{0} Init method.'.format(method_log_prefix))
    save = False

    flask_app = ctx.meta["flask_app"]

    with flask_app.test_request_context():
        context = _set_context()

        if dtype != 'save' and dtype != 'print':
            click.secho('{0} Please provide a valid type (save or print)'.format(method_log_prefix))
            sys.exit()
        else:
            if dtype == 'save':
                save = True
        time_period, calculation_date = _validate_time_period(method_log_prefix, time_period)
        if save:
            destination, filename = _validate_destination_filename(destination, filename, False, method_log_prefix)
        click.secho(destination)
        click.secho(filename)
        outfilename = tk.get_action('dge_dashboard_csv_published_datasets_by_root_org')(context,
                                                                                        {'date': str(calculation_date),
                                                                                        'import_date': time_period,
                                                                                        'save': save,
                                                                                        'destination': destination,
                                                                                        'filename': filename})
        if outfilename:
            click.secho('Writed json with {0} data in {1}'.format(dtype, outfilename))
        else:
            click.echo('No file was created')

    click.secho('{0} End method'.format(method_log_prefix))