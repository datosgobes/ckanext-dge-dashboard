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

ckan.module('dge_dashboard_adm_drupalTop10VotedDatasets', function ($, _) {
  return {
    initialize: function () {
      var top10vd_data_provider = this.options.data_provider;
      jsGrid.locale(this.options.language);
      var gridId = "#" + this.options.divid;
      var contents_by_likes_grid = new jsGrid.Grid($(gridId), {
        fields: [
          {
            name: "link",
            type: "string", 
            width: "70%",
            filtering:false, 
            title: this.options.column_titles[0]
          },
          { 
            name: "likes",
            type: "number", 
            width:  "30%",
            filtering:false,
            align: "center",  
            title: this.options.column_titles[2]
          }
        ],
        data: top10vd_data_provider,
        loadData: function (filter) {
            filter = filter || (this.filtering ? this.getFilter() : {});
            $.extend(filter, this._loadStrategy.loadParams(), this._sortingParams());
            var args = this._callEventHandler(this.onDataLoading, {
                filter: filter
            });
            return this._controllerCall("loadData", filter, args.cancel, function (loadedData) {
                if (!loadedData)
                    return;
                this._loadStrategy.finishLoad(loadedData);
                this._callEventHandler(this.onDataLoaded, {
                    data: loadedData
                });
                $(gridId).jsGrid("sort", "likes");
            });
        },
        width: "70%",
        height: "auto",
        filtering: false,
        selecting: false,
        sorting: true,
        autoload: true,

        paging: true,
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
