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

ckan.module("dge_dashboard_adm_numPublishersByMonthYear", function ($, _) {
  return {
    initialize: function () {
      var chart_anpbmy = AmCharts.makeChart(this.options.divid, {
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
        "plotAreaBorderAlpha": 0,
        "legend": {
          "align": "center",
          "equalWidths": false,
          "valueAlign": "left",
          "valueText": "[[value]] ([[percents]]%)",
          "valueWidth": 100,
          "useGraphSettings": true
        },
        "valueAxes": [{
          "stackType": "100%",
          "gridAlpha": 0.07,
          "position": "left",
          "title": this.options.title
        }],
        "chartCursor": {
          "cursorAlpha": 0,
          "zoomable": false,
          "valueLineEnabled": true,
          "valueLineBalloonEnabled": true,
          "valueLineAlpha": 0.5,
          "fullWidth": true,
          "categoryBalloonDateFormat": (this.options.language == "en")?"YYYY MMM":"MMM YYYY"
        },
        "valueScrollbar": {
          "oppositeAxis": true,
          "offset": 30,
          "scrollbarHeight": 10
        },
        "dataDateFormat": "YYYY-MM",
        "categoryField": "year",
        "categoryAxis": {
          "minPeriod": "MM",
          "parseDates": true,
          "equalSpacing": true,
          "minorGridAlpha": 0.1,
          "minorGridEnabled": true,
          "startOnAxis": true,
          "gridAlpha": 0.07,
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
                var date = new Date(Date.parse(currentDataValue.year));
                date.setMonth(date.getMonth() + 1);
                date.setDate(0);
                var monthOffset = (date.getMonth()<9)?"0":"";
                currentDataValue.year = date.getFullYear()+"-"+monthOffset+(date.getMonth()+1)+"-"+date.getDate();
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
              var this_chart = e.chart
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
              var this_chart = e.chart
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