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

ckan.module('dge_dashboard_org_mostVisitedDatasets', function ($, _) {
  return {
    initialize: function () {
      var omvd_data_provider = this.options.data_provider;
      var omvd_filter_div = "#"+this.options.filter_divid;
      var omvd_filter_values = this.options.filter_values;
      jsGrid.locale(this.options.language);
      var omvd_grid = new jsGrid.Grid($("#" + this.options.divid), {
        fields: [
          { 
            name: "month_id", 
            type: "select", 
            width: 100, 
            items: this.options.filter_values, 
            valueField: "id",  
            textField: "name", 
            selectedIndex: 0, 
            filtering:true, 
            title: this.options.column_titles[0],
            valueType: "string",
            visible:false
          },
          { 
            name: "package", 
            type: "text", 
            width: "40%", 
            filtering:false, 
            title: this.options.column_titles[1]
          },
          { 
            name: "publisher", 
            type: "text", 
            width: "40%", 
            filtering:false, 
            title: this.options.column_titles[2]
          },
          { 
            name: "visits", 
            type: "number", 
            width: "10%", 
            filtering:false, 
            title: this.options.column_titles[3], 
            align: "center"
          },
          { 
            name: "downloads", 
            type: "number", 
            width: "10%", 
            filtering:false, 
            title: this.options.column_titles[4], 
            align: "center"
          }
        ],
        data: omvd_data_provider, 
        width: "100%",
        height: "auto",
        filtering: false,
        selecting: false,
        sorting: true,
        autoload: true,
        noDataContent: this.options.no_data,
        controller: {
          loadData: function (filter) {
            var result = $.grep(omvd_data_provider, function(item, idx) {
              for (var key in filter) {
                var value = filter[key];
                if (value.length > 0) {
                  if (item[key].indexOf(value) == -1)
                    return false;
                }
              }
              return true;
            });
            return result;
          },
        }
      });
      $(omvd_filter_div).on("change", function(){
        var value = $(this).val();
        omvd_grid.loadData({'month_id': value});
      });
      omvd_grid.loadData({'month_id': omvd_filter_values[0]['id']});
    }
  }
});