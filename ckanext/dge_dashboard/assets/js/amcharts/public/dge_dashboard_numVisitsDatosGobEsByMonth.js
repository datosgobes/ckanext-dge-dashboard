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

ckan.module('dge_dashboard_numVisitsDatosGobEsByMonth', function ($, _) {
  return {
    initialize: function () {
      var chart_nvdgebm = AmCharts.makeChart(this.options.divid, {
        "type": "serial",
        "theme": "light",
        "language": this.options.language,
        "dataProvider": this.options.data_provider,
        "marginTop": 20,
        "marginBottom": 20,
        "marginRight": 70,
        "marginLeft": 70,
        "valueAxes": [{
          "axisAlpha": 0,
          "dashLength": 4,
          "position": "left"
        }],
        "numberFormatter": {
          "precision": -1,
          "decimalSeparator": (this.options.language == "en")?".":",",
          "thousandsSeparator": ""
        },
        "graphs": [{
          "id": "g1",
          "balloonText": "<div style='margin:10px; text-align:left;'><span style='font-size:13px'>[[category]]</span><br><span style='font-size:18px'>[[value]]</span>",
          "customBullet": "/amcharts/data/images/star.png?x",
          "customBulletField": "customBullet",
          "bulletSize": 14,
          "lineThickness": 1,
          "negativeLineColor": "#637bb6",
          "valueField": "value",
          "connect": true,
        }],
        "titles": [
          {"text": this.options.title}
        ],
        "chartScrollbar": {
          "graph": "g1",
          "gridAlpha": 0,
          "color": "#888888",
          "scrollbarHeight": 55,
          "backgroundAlpha": 0,
          "selectedBackgroundAlpha": 0.1,
          "selectedBackgroundColor": "#888888",
          "graphFillAlpha": 0,
          "autoGridCount": true,
          "selectedGraphFillAlpha": 0,
          "graphLineAlpha": 0.2,
          "graphLineColor": "#c2c2c2",
          "selectedGraphLineColor": "#888888",
          "selectedGraphLineAlpha": 1
        },
        "chartCursor": {
          "graphBulletSize": 1.5,
          "cursorAlpha": 0,
          "valueLineEnabled": true,
          "valueLineBalloonEnabled": true,
          "valueLineAlpha": 0.5,
          "fullWidth": true,
          "categoryBalloonDateFormat": (this.options.language == "en")?"YYYY MMM":"MMM YYYY"
        },
        "autoMargins": false,
        "dataDateFormat": "YYYY-MM",
        "categoryField": "date",
        "valueScrollbar": {
          "oppositeAxis": true,
          "offset": 30,
          "scrollbarHeight": 10
        },
        "categoryAxis": {
          "minPeriod": "MM",
          "parseDates": true,
          "equalSpacing": true,
          "axisAlpha": 0,
          "gridAlpha": 0,
          "inside": false,
          "tickLength": 0,
          "minorGridAlpha": 0.1,
          "minorGridEnabled": true,
          "startOnAxis": true,
          "dateFormats": [
            {period:'YYYY-MM',format:'MMM YY'},
            {period: 'MM',format: 'MMM YY'},
            {period: 'YYYY', format: 'MMM YY'}
          ]
        },
        "export": {
          "enabled": true,
          "processData": function(data, cfg) {
            //only for JSON and XLSX export.
            if ((cfg.format === "JSON" || cfg.format === "XLSX") && !cfg.ignoreThatRequest) {
              data.forEach(function(currentDataValue) {
                var date = new Date(Date.parse(currentDataValue.date));
                date.setMonth(date.getMonth() + 1);
                date.setDate(0);
                var monthOffset = (date.getMonth()<9)?"0":"";
                currentDataValue.date = date.getFullYear()+"-"+monthOffset+(date.getMonth()+1)+"-"+date.getDate();
              });
            }
            return data;
          }
        }, 
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
              function zoomChart(){
                this_chart.zoomToIndexes(Math.round(this_chart.dataProvider.length * 0), Math.round(this_chart.dataProvider.length * 1));
              }
              if (this_chart.dataProvider == undefined || 
                  this_chart.dataProvider.length == 0) {
                this_chart.labelsEnabled = false;
                this_chart.addLabel("50%", "50%", e.chart.noDataLabel, "middle", 15);
                this_chart.alpha = 0.3;
              }
              zoomChart();
            }
          }
        ]
      });
    }
  };
});