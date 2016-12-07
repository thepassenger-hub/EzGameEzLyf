import { Component } from '@angular/core';
import { ResultsListComponent } from './results-list.component';
import { ResultsListService }   from './services/results-list.service';
import { TestComponent }        from './test.component';
@Component({
  selector: 'my-app',
  template: `<h1>{{title}}</h1>
             <results></results>`,
  directives: [ResultsListComponent],
  providers: [ResultsListService]
})
export class AppComponent  { 
  title = 'Angular 2 Test'; 
}
