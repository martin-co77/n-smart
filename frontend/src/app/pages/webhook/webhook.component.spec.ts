import {WebhookComponent} from "./webhook.component";
import {ComponentFixture, fakeAsync, inject, TestBed, tick} from "@angular/core/testing";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {LocalStorageModule} from "angular-2-local-storage";
import {MatDialogModule} from "@angular/material/dialog";
import {HttpClientTestingModule, HttpTestingController} from "@angular/common/http/testing";
import {AppConfig} from "../../app.config";
import {TokenProvider} from "../../providers/token.provider";


describe('Webhook component', () => {
  let component: WebhookComponent;
  let fixture: ComponentFixture<WebhookComponent>;
  let table: HTMLElement;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WebhookComponent],
      providers: [TokenProvider],
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
        LocalStorageModule.forRoot(),
        MatDialogModule
      ]
    });
    fixture = TestBed.createComponent(WebhookComponent);
    component = fixture.componentInstance;
    table = fixture.nativeElement.querySelector('table');
  });

  it('should create the component', () => {
    expect(component).toBeDefined()
  })

  it('should have table within the page', () => {
    expect(table.innerHTML).toContain('Event Type')
  })

  it('should issue a request to fetch alerts', fakeAsync(inject(
    [HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
      let fakeResponse = {status: 200, statusText: 'success'};
      component.loadWebhook()

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/webhook`,
        method: 'GET'
      });

      requestWrapper.flush({data: [], status: true, statusText: 'success'}, fakeResponse);
      tick()
      expect(requestWrapper.request.method).toEqual('GET');
    })))


  it('should verify deleting webhook', fakeAsync(inject(
    [HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
      let fakeResponse = {status: 201, statusText: 'success'};
      let response = null;
      component.deleteWebHook(1)

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/webhook/1`,
        method: 'DELETE'
      });

      requestWrapper.flush({data: [], status: true, statusText: 'success'}, fakeResponse);
      tick()
      expect(requestWrapper.request.method).toEqual('DELETE');
    })))
})

