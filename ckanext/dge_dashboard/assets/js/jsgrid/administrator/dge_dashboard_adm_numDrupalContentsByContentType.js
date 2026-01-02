/*
* Copyright (C) 2025 Entidad Pública Empresarial Red.es
*
* This file is part of "dge-dashboard (datos.gob.es)".
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 2 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

"use strict";

ckan.module('dge_dashboard_adm_numDrupalContentsByContentType', function ($, _) {
  return {
    initialize: function () {
      var andcbbt_data_provider = this.options.data_provider;
      jsGrid.locale(this.options.language);
      var andcbbt_grid = new jsGrid.Grid($("#" + this.options.divid), {
        fields: [
          {
            name: "content_type", 
            type: "string", 
            width: "60%", 
            filtering:false, 
            title: this.options.column_titles[0]
          },
          { 
            name: "num_contents", 
            type: "number", 
            width:  "40%", 
            filtering:false,
            align: "center",  
            title: this.options.column_titles[1]
          }
        ],
        data: andcbbt_data_provider, 
        width: "45%",
        height: "auto",
        filtering: false,
        selecting: false,
        sorting: true,
        autoload: true,

        paging: false,
        pageSize: 10,
        pageButtonCount: 5,
        pagerContainer: "#" + this.options.pager_divid,
        pageNavigatorNextText: "&#8230;",
        pageNavigatorPrevText: "&#8230;",

        noDataContent: this.options.no_data,
      });
    }
  }
});