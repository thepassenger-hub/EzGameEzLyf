"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var results_list_service_1 = require('./services/results-list.service');
var ResultsListComponent = (function () {
    function ResultsListComponent(resultsListService) {
        this.resultsListService = resultsListService;
    }
    ResultsListComponent.prototype.getGames = function () {
        var _this = this;
        this.resultsListService
            .getGames()
            .then(function (games) { return _this.games = games; })
            .catch(function (error) { return _this.error = error; });
    };
    ResultsListComponent.prototype.ngOnInit = function () {
        this.getGames();
    };
    ResultsListComponent = __decorate([
        core_1.Component({
            selector: 'results',
            templateUrl: '/app/results-list.component.html',
        }), 
        __metadata('design:paramtypes', [results_list_service_1.ResultsListService])
    ], ResultsListComponent);
    return ResultsListComponent;
}());
exports.ResultsListComponent = ResultsListComponent;
//# sourceMappingURL=results-list.component.js.map