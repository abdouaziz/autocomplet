import { Injectable } from '@angular/core';
import {Http} from '@angular/http'
import {map} from 'rxjs/operators'
 
@Injectable({
  providedIn: 'root'
})
export class ServiceService {

  
  constructor(public http:Http) { }

  save(contact:any){

    return this.http.post("http://localhost:5000/suggest",contact)
      .pipe(map(resp=>resp.json()))

  }




  
 

  

}
