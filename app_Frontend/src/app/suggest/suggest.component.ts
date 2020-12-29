import { Component, OnInit } from '@angular/core';
import { ServiceService } from '../service.service';

@Component({
  selector: 'app-suggest',
  templateUrl: './suggest.component.html',
  styleUrls: ['./suggest.component.css']
})
export class SuggestComponent implements OnInit { 


  resp:any
  suggest = []
 
  message :any
 
  constructor(public service :ServiceService) { }

  ngOnInit(): void {
  } 



  onAdd(c){
    console.log(c)
    this.service.save(c)
    
    .subscribe(data => {
      this.resp=data 

      for (let i=0 ; i< this.resp.length ; i++){
        this.suggest.push(this.resp[i][0])


      }

      console.log("les donneés ",this.resp)
       
    } , err=>{
      console.log("errerur ",err) ;
    });
  }




}
