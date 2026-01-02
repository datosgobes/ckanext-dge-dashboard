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

# encoding: utf-8
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckan.lib.plugins import DefaultTranslation
from ckanext.dge_dashboard import helpers
from routes.mapper import SubMapper
from ckan.plugins.toolkit import config

from ckanext.dge_dashboard.views.flask_plugin import ( DGEDashboardPlugins )

import logging

log = logging.getLogger(__name__)

def is_frontend():
    is_frontend = False
    config_is_frontend = config.get('ckanext.dge.is_frontend', None)
    if config_is_frontend and config_is_frontend.lower() == 'true': 
        is_frontend = True  
    return is_frontend

class DgeDashboardPlugin(DGEDashboardPlugins, plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)

    if is_frontend(): 
        log.debug('IS_FRONTEND')
        plugins.implements(plugins.IConfigurer, inherit=True)
        plugins.implements(plugins.ITranslation, inherit=True)
        plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        if is_frontend():
            toolkit.add_public_directory(config_, 'public')
            toolkit.add_template_directory(config_, 'templates')
            toolkit.add_resource('assets', 'dge_dashboard')

    # ############### ITemplateHelpers ####################################### #

    def get_helpers(self):
        return {
            'dge_dashboard_data_num_datasets_by_month_year': helpers.dge_dashboard_data_num_datasets_by_month_year,
            'dge_dashboard_data_num_datasets_by_administration_level': helpers.dge_dashboard_data_num_datasets_by_administration_level,
            'dge_dashboard_data_distribution_format': helpers.dge_dashboard_data_distribution_format,
            'dge_dashboard_data_distribution_format_by_administration_level': helpers.dge_dashboard_data_distribution_format_by_administration_level,
            'dge_dashboard_data_num_datasets_by_category': helpers.dge_dashboard_data_num_datasets_by_category,
            'dge_dashboard_data_num_drupal_contents': helpers.dge_dashboard_data_num_drupal_contents,
            'dge_dashboard_data_num_visits': helpers.dge_dashboard_data_num_visits,
            'dge_dashboard_data_most_visited_datasets': helpers.dge_dashboard_data_most_visited_datasets,
            'dge_get_visibility_of_public_graphs': helpers.dge_get_visibility_of_public_graphs,

            'dge_dashboard_organization_data_num_datasets_by_month_year': helpers.dge_dashboard_organization_data_num_datasets_by_month_year,
            'dge_dashboard_organization_data_distribution_format': helpers.dge_dashboard_organization_data_distribution_format,
            'dge_dashboard_organization_data_users': helpers.dge_dashboard_organization_data_users,
            'dge_dashboard_organization_data_assigned_requests': helpers.dge_dashboard_organization_data_assigned_requests,
            'dge_dashboard_organization_data_num_comments_by_month_year': helpers.dge_dashboard_organization_data_num_comments_by_month_year,
            'dge_dashboard_organization_data_most_visited_datasets': helpers.dge_dashboard_organization_data_most_visited_datasets,

            'dge_dashboard_administrator_data_num_datasets_by_administration_level': helpers.dge_dashboard_administrator_data_num_datasets_by_administration_level,
            'dge_dashboard_administrator_data_num_datasets_by_organization': helpers.dge_dashboard_administrator_data_num_datasets_by_organization,
            'dge_dashboard_administrator_data_num_datasets_by_num_resources': helpers.dge_dashboard_administrator_data_num_datasets_by_num_resources,
            'dge_dashboard_administrator_data_num_publishers_by_month_year': helpers.dge_dashboard_administrator_data_num_publishers_by_month_year,
            'dge_dashboard_administrator_data_assigned_requests': helpers.dge_dashboard_administrator_data_assigned_requests,
            'dge_dashboard_administrator_data_users': helpers.dge_dashboard_administrator_data_users,
            'dge_dashboard_administrator_data_users_by_adm_level': helpers.dge_dashboard_administrator_data_users_by_adm_level,
            'dge_dashboard_administrator_published_drupal_contents': helpers.dge_dashboard_administrator_published_drupal_contents,
            'dge_dashboard_administrator_data_num_comments_by_month_year': helpers.dge_dashboard_administrator_data_num_comments_by_month_year,
            'dge_dashboard_administrator_data_num_visits_by_section': helpers.dge_dashboard_administrator_data_num_visits_by_section,
            'dge_dashboard_administrator_datasets_by_org': helpers.dge_dashboard_administrator_datasets_by_org,
            'dge_dashboard_administrator_data_num_publishers_by_administration_level': helpers.dge_dashboard_administrator_data_num_publishers_by_administration_level,
            'dge_dashboard_administrator_organizations_by_level': helpers.dge_dashboard_administrator_organizations_by_level,
			'dge_dashboard_administrator_drupal_contents_by_likes': helpers.dge_dashboard_administrator_drupal_contents_by_likes,
            'dge_dashboard_administrator_drupal_top10_voted_datasets': helpers.dge_dashboard_administrator_drupal_top10_voted_datasets,

            'dge_dashboard_get_month': helpers.dge_dashboard_get_month,
            'dge_dashboard_special_org': helpers.dge_dashboard_special_org,
            }

    ## IActions

    def get_actions(self):

        module_root = 'ckanext.dge_dashboard.logic.action'
        action_functions = _get_logic_functions(module_root)

        return action_functions

    ## IAuthFunctions

    def get_auth_functions(self):

        module_root = 'ckanext.dge_dashboard.logic.auth'
        auth_functions = _get_logic_functions(module_root)

        return auth_functions

def _get_logic_functions(module_root, logic_functions = {}):

    for module_name in ['get', 'update']:
        module_path = '%s.%s' % (module_root, module_name,)

        module = __import__(module_path)

        for part in module_path.split('.')[1:]:
            module = getattr(module, part)

        for key, value in list(module.__dict__.items()):
            if not key.startswith('_') and  (hasattr(value, '__call__')
                        and (value.__module__ == module_path)):
                logic_functions[key] = value

    return logic_functions