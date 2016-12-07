import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } 	 from '@angular/forms';			
import { HttpModule } 	 from '@angular/http';

import { AppComponent } from './app.component'
import { ResultsListComponent } from './results-list.component';
import { ResultsListService }   from './services/results-list.service';

@NgModule({
  imports:      [ 
	BrowserModule,
	FormsModule,
	HttpModule,
  ],
  declarations: [ AppComponent, ResultsListComponent,],
  bootstrap:    [ AppComponent ],
  providers: 	[ ResultsListService ],
})

export class AppModule { }