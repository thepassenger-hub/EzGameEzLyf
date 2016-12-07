import { Injectable }               from '@angular/core';
import { Http }                     from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class ResultsListService {
    private apiURL = 'http://localhost:8000/api/search/?q=killing+floor+2';

    constructor(private http: Http) {}

    getGames() {
        return this.http.get(this.apiURL)
               .toPromise() 
               .then(response => response.json())
               .catch(this.handleError);
    }
    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }

}