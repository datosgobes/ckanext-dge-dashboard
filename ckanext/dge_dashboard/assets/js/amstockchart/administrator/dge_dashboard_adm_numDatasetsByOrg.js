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

ckan.module('dge_dashboard_adm_numDatasetsByOrg', function ($, _) {
  return {
    initialize: function () {
      var andbo = AmCharts.makeChart( this.options.divid, {
        "type": "stock",
        "theme": "light",
        "language": this.options.language,
        "marginTop": 20,
        "marginBottom": 20,
        "marginRight": 70,
        "marginLeft": 70,
        "dataDateFormat": "YYYY-MM",
        "dataSets": this.options.data_sets,
        "categoryAxesSettings": {
          "minPeriod": "MM",
          "parseDates": true,
          "equalSpacing": true,
          "minorGridAlpha": 0.1,
          "minorGridEnabled": true,
          "inside": false,
          "groupToPeriods": ['MM'],
          "dateFormats": [
            {period:'YYYY-MM',format:'MMM YY'},
            {period: 'MM',format: 'MMM YY'},
            {period: 'YYYY', format: 'MMM YY'}
          ]
        },
        "panels": [ {
          "showCategoryAxis": true,
          "title":  this.options.title,
          "decimalSeparator": (this.options.language == "en")?".":",",
          "thousandsSeparator": "",
          "valueAxes": [{
            "axisAlpha": 0,
            "position": "left",
            "integersOnly": true
          }],
          "stockGraphs": [ {
            "id": "g1",
            "valueField": "value",
            "comparable": true,
            "compareField": "value",
            "dateFormat": "YYYY-MM",
            "bullet": "round",
            "bulletBorderColor": "#FFFFFF",
            "bulletBorderAlpha": 1,
            "categoryBalloonDateFormat": "YYYY-MM",
            "balloonText": "[[value]]",
            "compareGraphBalloonText": "[[category]]XXXXXX2->[[title]]:<b>[[value]]</b>",
            "compareGraphBullet": "round",
            "compareGraphBulletBorderColor": "#FFFFFF",
            "compareGraphBulletBorderAlpha": 1,
            "balloonDateFormat": (this.options.language == "en")?"YYYY MMM":"MMM YYYY",
            "lineThickness": 3,
            "compareGraphLineThickness": 3,
            "balloonFunction": function(graphDataItem, graph) {
              var value = "<b>"+graphDataItem.graph.legendTextReal + "</b><br>";
              AmCharts.shortMonthNames = andbo.shortMonthNames;
              value = value + AmCharts.formatDate(graphDataItem.dataContext.year, "MMM YYYY");
              value = value + ": " + graphDataItem.values.value;
              return value;
            },
            "compareGraphBalloonFunction": function(graphDataItem, graph) {
              var value = "<b>"+graphDataItem.graph.legendTextReal + "</b><br>";
              AmCharts.shortMonthNames = andbo.shortMonthNames;
              value = value + AmCharts.formatDate(graphDataItem.dataContext.year, "MMM YYYY");
              value = value + ": " + graphDataItem.values.value;
              return value;
            }
          } ],
          "stockLegend": {
            "periodValueTextComparing": "[[percents.value.close]]%",
            "periodValueTextRegular": "[[value.close]]",
            "useGraphSettings": true
          }
        } ],
        "panelsSettings": {
          "decimalSeparator": (this.options.language == "en")?".":",",
          "percentPrecision": 2,
          "precision": -1,
          "thousandsSeparator": "",
          "zoomOutAxes": true,
          "recalculateToPercents": "never"
        },
        "chartScrollbarSettings": {
          "graph": "g1"
        },
        "chartCursorSettings": {
          "valueBalloonsEnabled": true,
          "fullWidth": true,
          "cursorAlpha": 0.1,
          "valueLineBalloonEnabled": true,
          "valueLineEnabled": true,
          "valueLineAlpha": 0.5,
          "categoryBalloonDateFormats":[{period:'YYYY-MM',format:(this.options.language == "en")?"YYYY MMM":"MMM YYYY"}]
        },
        "dataSetSelector": {
          "position": "top",
          "comboBoxSelectText": this.options.combo_box_select_text,
          "compareText": this.options.compare_text,
          "selectText": this.options.select_text
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
              if (this_chart.dataSets == undefined || 
                  this_chart.dataSets.length == 0) {
                this_chart.panels[0].labelsEnabled = false;
                this_chart.panels[0].addLabel("50%", "50%", e.chart.noDataLabel, "middle", 15);
                this_chart.alpha = 0.3;
              }
            }
          },
          {
            "event": "rendered",
            "method": function(e) { 
              var this_chart = e.chart
              if (this_chart.dataSets == undefined || 
                  this_chart.dataSets.length == 0) {
                this_chart.panels[0].labelsEnabled = false;
                this_chart.panels[0].addLabel("50%", "50%", e.chart.noDataLabel, "middle", 15);
                this_chart.alpha = 0.3;
              }
            }
          }
        ]
      });
    }
  };
});