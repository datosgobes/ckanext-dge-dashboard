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

// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";
var chart_dfbal;
ckan.module('dge_dashboard_distributionFormatByAdministrationLevel', function ($, _) {
  return {
    initialize: function () {
      chart_dfbal = AmCharts.makeChart(this.options.divid, {
        "type": "pie",
        "theme": "light",
        "startDuration": 0,
        "maxLabelWidth": 110,
        "language": this.options.language,
        "addClassNames": true,
        "globalText": ((this.options.data_text_2)?"\n" + this.options.data_text_2:""),
        "balloonText": "[[title]]<br><span style='font-size:14px'><b>[[value]]</b> ([[percents]]%)</span>",
        "labelText": "[[title]]: [[value]] ([[percents]]%)",
        "titles": [
          {"text": this.options.title},
        ], 
        "allLabels": [{
          "y": "50%",
          "align": "center",
          "size": "50%",
          "bold": true,
          "text": ((this.options.data_text_1)?this.options.data_text_1:"") + 
                  ((this.options.data_text_2)?"\n" + this.options.data_text_2:""),
          "color": "#555"
        }],
        "numberFormatter": {
          "precision": -1,
          "decimalSeparator": (this.options.language == "en")?".":",",
          "thousandsSeparator": ""
        },
        "innerRadius": "45%",
        "pullOutRadius": 20,
        "defs": {
          "filter": [{
            "id": "shadow",
            "width": "200%",
            "height": "200%",
            "feOffset": {
              "result": "offOut",
              "in": "SourceAlpha",
              "dx": 0,
              "dy": 0
            },
            "feGaussianBlur": {
              "result": "blurOut",
              "in": "offOut",
              "stdDeviation": 5
            },
            "feBlend": {
              "in": "SourceGraphic",
              "in2": "blurOut",
              "mode": "normal"
            }
          }]
        },
        "dataProvider": this.options.data_provider,
        "groupedTitle": this.options.grouped_title,
        "groupPercent": this.options.group_percent,
        "valueField": "value",
        "titleField": "format",
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
function setDataSet(data, label_text){
  chart_dfbal.dataProvider = data;
  chart_dfbal.allLabels[0].text = ((label_text)?label_text:"") + chart_dfbal.globalText;
  chart_dfbal.validateData();
}