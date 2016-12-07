import { Component, OnInit }         from '@angular/core';
import { ResultsListService }        from './services/results-list.service';

@Component({
    selector: 'results',
    templateUrl: '/app/results-list.component.html',
})
export class ResultsListComponent implements OnInit {

    games: any[];
    error: any;
    constructor(private resultsListService: ResultsListService) { }

    getGames() {
        this.resultsListService
            .getGames()
            .then(games => this.games = games)
            .catch(error => this.error = error);
    }

    ngOnInit() {
        this.getGames();
    }
}