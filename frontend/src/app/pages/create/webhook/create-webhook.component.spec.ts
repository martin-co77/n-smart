import {CreateWebHookComponent} from "./create-webhook.component";
import {ComponentFixture, fakeAsync, inject, TestBed, tick} from "@angular/core/testing";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {HttpClientTestingModule, HttpTestingController} from "@angular/common/http/testing";
import {MatDialogModule, MatDialogRef} from "@angular/material/dialog";
import {TokenProvider} from "../../../providers/token.provider";
import {LocalStorageModule} from "angular-2-local-storage";
import {AppConfig} from "../../../app.config";

describe('Create webhook', () => {
  let fixture: ComponentFixture<CreateWebHookComponent>
  let component: CreateWebHookComponent;
  beforeEach(() => {

    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
        MatDialogModule,
        LocalStorageModule.forRoot()],
      providers: [TokenProvider, {provide : MatDialogRef, useFactory: () => jasmine.createSpyObj('MatDialogRef', ['close', 'afterClosed']) }],
      declarations: [CreateWebHookComponent]
    })

    fixture = TestBed.createComponent(CreateWebHookComponent)
    component = fixture.componentInstance
  })

  it('should create the component', () => {
    expect(component).toBeDefined()
  })

  it('should have markup within the page', () => {
    expect(fixture.nativeElement.innerHTML).toContain('value="speech">Speech</option>')
  })

  it('should create webhook', fakeAsync(inject(
    [HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
      let fakeResponse = {status: 200, statusText: 'success'};
      const fakeEmail = 'test@example.org'
      component.deviceForm = {
        valid: true,
        pristine: false,
        controls: {
          type: {
            value: 'speech'
          },
          name: {
            value: 'test device'
          },
          url: {
            value: 'http://test.com/respond'
          },
        }
      } as any
      component.createDevice()

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/webhook`,
        method: 'POST'
      });

      requestWrapper.flush({data: {}, status: true, statusText: 'success'}, fakeResponse);
      tick()
      expect(requestWrapper.request.method).toEqual('POST');
      expect(requestWrapper.request.url).toEqual(`${AppConfig.endpoint}/webhook`)
      expect(requestWrapper.request.body).toEqual({
        event: 'speech',
        name: 'test device',
        url: 'http://test.com/respond'
      })
    })));
})
