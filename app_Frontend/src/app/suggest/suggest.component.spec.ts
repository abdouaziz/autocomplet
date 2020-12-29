import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SuggestComponent } from './suggest.component';

describe('SuggestComponent', () => {
  let component: SuggestComponent;
  let fixture: ComponentFixture<SuggestComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SuggestComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SuggestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
