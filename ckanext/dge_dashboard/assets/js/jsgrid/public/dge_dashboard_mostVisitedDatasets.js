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

ckan.module('dge_dashboard_mostVisitedDatasets', function ($, _) {
  return {
    initialize: function () {
      var mvd_data_provider = this.options.data_provider;
      var mvd_filter_div = "#"+this.options.filter_divid;
      var mvd_filter_values = this.options.filter_values;
      jsGrid.locale(this.options.language);
      var mvd_grid = new jsGrid.Grid($("#" + this.options.divid), {
        fields: [
          { 
            name: "month_id", 
            type: "select", 
            width: 100, 
            items: mvd_filter_values, 
            valueField: "id",  
            textField: "name", 
            selectedIndex: 0, 
            filtering:true, 
            title: this.options.column_titles[0],
            valueType: "string",
            visible: false
          },
          { 
            name: "order", 
            type: "number", 
            width: "10%", 
            filtering:false, 
            align: "center", 
            title: this.options.column_titles[1]
          },
          { 
            name: "package", 
            type: "text", 
            width: "45%", 
            filtering:false, 
            title: this.options.column_titles[2]
          },
          { 
            name: "publisher", 
            type: "text", 
            width: this.options.visible_col_visits ? "30%" : "45%", 
            filtering:false, 
            title: this.options.column_titles[3]
          },
          { 
            name: "visits", 
            type: "number", 
            width: "15%", 
            filtering:false, 
            title: this.options.column_titles[4], 
            align: "center", 
            visible:this.options.visible_col_visits
          }
        ],
        data: mvd_data_provider, 
        width: "100%",
        height: "auto",
        filtering: false,
        selecting: false,
        sorting: true,
        autoload: true,
        noDataContent: this.options.no_data,
        controller: {
          loadData: function (filter) {
            var result = $.grep(mvd_data_provider, function(item, idx) {
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
      $(mvd_filter_div).on("change", function(){
        var value = $(this).val();
        mvd_grid.loadData({'month_id': value});
      });
      mvd_grid.loadData({'month_id': mvd_filter_values[0]['id']});
    }
  }
});