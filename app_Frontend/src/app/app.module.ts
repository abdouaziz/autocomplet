import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SuggestComponent } from './suggest/suggest.component';
import { FormsModule } from '@angular/forms';
import { ServiceService } from './service.service';
import {HttpClientModule} from '@angular/common/http'
import {HttpModule} from '@angular/http'

@NgModule({
  declarations: [
    AppComponent,
    SuggestComponent,
  
  ],
  imports: [
    BrowserModule,
    AppRoutingModule ,
    FormsModule ,
    HttpClientModule ,
    HttpModule
    
  ],
  providers: [ServiceService],
  bootstrap: [AppComponent]
})
export class AppModule { }
