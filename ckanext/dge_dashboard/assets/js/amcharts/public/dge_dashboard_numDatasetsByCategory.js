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

ckan.module("dge_dashboard_numDatasetsByCategory", function ($, _) {

  return {
    initialize: function () {
      var chart_ndbc = AmCharts.makeChart(this.options.divid, {
        "type": "serial",
        "theme": "light",
        "language": this.options.language,
        "marginTop": 20,
        "marginBottom": 20,
        "marginRight": 70,
        "marginLeft": 70,
        "colors":[
          "#b5e0f2"
        ],
        "numberFormatter": {
          "precision": -1,
          "decimalSeparator": (this.options.language == "en")?".":",",
          "thousandsSeparator": ""
        },
        "dataProvider": this.options.data_provider,
        "graphs": [{
          "balloonText": "[[category]]:[[value]]",
          "fillAlphas": 1,
          "lineAlpha": 0.2,
          "type": "column",
          "valueField": "value"
        }],
        "depth3D": 20,
        "angle": 30,
        "rotate": false,
        "valueAxes": [{
          "title": this.options.title
        }],
        "categoryField": "theme",
        "categoryAxis": {
          "gridPosition": "start",
          "fillAlpha": 0.05,
          "position": "left",
          "labelRotation": 40,
        },
        "export": {"enabled": true}, 
        "responsive": {"enabled": true},
        "noDataLabel": this.options.no_data,
        "listeners": [
          {
            "event": "init",
            "method": function(e) { 
              if (e.chart.dataProvider == undefined || 
                  e.chart.dataProvider.length == 0) {
                this_chart.labelsEnabled = false;
                this_chart.addLabel("50%", "50%", e.chart.noDataLabel, "middle", 15);
                this_chart.alpha = 0.3;
              }
            }
          },
          {
            "event": "rendered",
            "method": function(e) { 
              if (e.chart.dataProvider == undefined || 
                  e.chart.dataProvider.length == 0) {
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