import {ComponentFixture, fakeAsync, inject, TestBed, tick} from "@angular/core/testing";
import {DashboardComponent} from "./dashboard.component";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {HttpClientTestingModule, HttpTestingController} from "@angular/common/http/testing";
import {LocalStorageModule} from "angular-2-local-storage";
import {TokenProvider} from "../../providers/token.provider";
import {MatDialogModule} from "@angular/material/dialog";
import {AppConfig} from "../../app.config";

describe('Dashboard Component', () => {
  let fixture: ComponentFixture<DashboardComponent>;
  let component: DashboardComponent;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DashboardComponent],
      imports: [
        HttpClientModule, MatDialogModule, HttpClientTestingModule, LocalStorageModule.forRoot()],
      providers: [TokenProvider]
    })

    fixture = TestBed.createComponent(DashboardComponent)
    component = fixture.componentInstance;
  })


  it('should verify component was created', () => {
    expect(component).toBeDefined()
  })

  it('should verify that HTML sections are available within the page', () => {
    expect(fixture.nativeElement.querySelector('.table-container')).toBeTruthy()
  })

  it('should verify that data is requested via the API', fakeAsync(inject(
    [HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
        let fakeResponse = {status: 200, statusText: 'success'};
        component.loadDashboard()

        const requestWrapper = backend.expectOne({
          url: `${AppConfig.endpoint}/stat`,
          method: 'GET'
        });

        requestWrapper.flush({data: {
          'grammar': ['test']
          }, status: true, statusText: 'success'}, fakeResponse);
        tick()
        expect(requestWrapper.request.method).toEqual('GET');
        expect(requestWrapper.request.url).toEqual(`${AppConfig.endpoint}/stat`)
  })))

  it('should verify speech recognition is implemented and functional', fakeAsync(inject(
    [HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
      let fakeResponse = {status: 200, statusText: 'success'};
      const fakeWord = 'test test'
      window.confirm = jasmine.createSpy().and.callFake(() => {
        return true;
      })
      component.onSpeechResult(fakeWord)

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/webhook/incoming`,
        method: 'POST'
      });

      requestWrapper.flush({data: {
          'grammar': ['test']
        }, status: true, statusText: 'success'}, fakeResponse);
      tick()
      expect(requestWrapper.request.method).toEqual('POST');
      expect(requestWrapper.request.url).toEqual(`${AppConfig.endpoint}/webhook/incoming`)
      expect(requestWrapper.request.body).toEqual({event: 'speech', data: fakeWord})
  })))

})
