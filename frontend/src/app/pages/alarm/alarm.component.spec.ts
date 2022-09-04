import {AlarmComponent} from "./alarm.component";
import {ComponentFixture, fakeAsync, inject, TestBed, tick} from "@angular/core/testing";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {HttpClientTestingModule, HttpTestingController} from "@angular/common/http/testing";
import {TokenProvider} from "../../providers/token.provider";
import {LocalStorageModule} from "angular-2-local-storage";
import {MatDialogModule} from "@angular/material/dialog";
import {AppConfig} from "../../app.config";

describe('Alarm component', () => {
  let component: AlarmComponent;
  let fixture: ComponentFixture<AlarmComponent>;
  let table: HTMLElement;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AlarmComponent],
      providers: [TokenProvider],
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
        LocalStorageModule.forRoot(),
        MatDialogModule
      ]
    });
    fixture = TestBed.createComponent(AlarmComponent);
    component = fixture.componentInstance;
    table = fixture.nativeElement.querySelector('table');
  });

  it('should create the component', () => {
    expect(component).toBeDefined()
  })

  it('should have table within the page', () => {
    expect(table.innerHTML).toContain('Created At')
  })

  it('should issue a request to fetch alerts', fakeAsync(inject(
    [HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
      let fakeResponse = {status: 200, statusText: 'success'};
      component.loadAlerts()

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/alarm`,
        method: 'GET'
      });

      requestWrapper.flush({data: [], status: true, statusText: 'success'}, fakeResponse);
      tick()
      expect(requestWrapper.request.method).toEqual('GET');
  })))


  it('should verify deleting alert', fakeAsync(inject(
    [HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
      let fakeResponse = {status: 201, statusText: 'success'};
      let response = null;
      component.deleteAlarm(1)

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/alarm/1`,
        method: 'DELETE'
      });

      requestWrapper.flush({data: [], status: true, statusText: 'success'}, fakeResponse);
      tick()
      expect(requestWrapper.request.method).toEqual('DELETE');
    })))
})

