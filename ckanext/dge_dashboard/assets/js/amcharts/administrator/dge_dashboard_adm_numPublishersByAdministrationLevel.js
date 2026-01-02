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

// Enable JavaScript"s strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module("dge_dashboard_administrator_numPublishersByAdministrationLevel", function ($, _) {
  return {
    initialize: function () {
      var chart_anpbal = AmCharts.makeChart(this.options.divid, {
        "type": "serial",
        "theme": "light",
        "language": this.options.language,
        "marginTop": 20,
        "marginBottom": 20,
        "marginRight": 70,
        "marginLeft": 70,
        "numberFormatter": {
          "precision": -1,
          "decimalSeparator": (this.options.language == "en")?".":",",
          "thousandsSeparator": ""
        },
        "dataProvider": this.options.data_provider,
        "graphs": this.options.graphs,
        "categoryField": "category",
        "columnWidth": 0.8,
        "angle": 30,
        "depth3D": 30,
        "categoryAxis": {
          "gridPosition": "start",
          "startOnAxis": false
        },
        "trendLines": [],
        "guides": [],
        "valueAxes": [{
          "stackType": "regular",
          "title": this.options.title
        }],
        "allLabels": [],
        "ballon": [],
        "legend": {
          "enable": true,
          "align": "centre",
          "useGraphSettings": true
        },
        "titles": [],
        "export": {"enabled": true}, 
        "responsive": {"enabled": true},
        "noDataLabel": this.options.no_data,
        "listeners": [
          {
            "event": "init",
            "method": function(e) { 
              var this_chart = e.chart;
              if (this_chart.dataProvider == undefined || 
                  this_chart.dataProvider.length == 0) {
                this_chart.labelsEnabled = false;
                this_chart.addLabel("50%", "50%", e.chart.noDataLabel, "middle", 15);
                this_chart.alpha = 0.3;
              }
            }
          },
          {
            "event": "rendered",
            "method": function(e) { 
              var this_chart = e.chart;
              if (this_chart.dataProvider == undefined || 
                  this_chart.dataProvider.length == 0) {
                this_chart.labelsEnabled = false;
                this_chart.addLabel("50%", "50%", e.chart.noDataLabel, "middle", 15);
                this_chart.alpha = 0.3;
              }
            }
          }
        ]
      });
    }
  };
});