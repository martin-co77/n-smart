import {ComponentFixture, fakeAsync, inject, TestBed, tick} from "@angular/core/testing";
import {IntruderAlertComponent} from "./intruder-alert.component";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {HttpClientTestingModule, HttpTestingController} from "@angular/common/http/testing";
import {MatDialogModule, MatDialogRef} from "@angular/material/dialog";
import {TokenProvider} from "../../../providers/token.provider";
import {AppConfig} from "../../../app.config";
import {LocalStorageModule} from "angular-2-local-storage";

describe('Create Alarm', () => {
  let fixture: ComponentFixture<IntruderAlertComponent>
  let component: IntruderAlertComponent;
  beforeEach(() => {

    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
        MatDialogModule,
        LocalStorageModule.forRoot()],
      providers: [TokenProvider, {provide : MatDialogRef, useFactory: () => jasmine.createSpyObj('MatDialogRef', ['close', 'afterClosed']) }],
      declarations: [IntruderAlertComponent]
    })

    fixture = TestBed.createComponent(IntruderAlertComponent)
    component = fixture.componentInstance
  })


  it('should create the component', () => {
    expect(component).toBeDefined()
  })

  it('should have elements within the page', () => {
    expect(fixture.nativeElement.innerHTML).toContain(' class="text-white font-light ml-[5px]">Done</span>')
  })

  it('should create alert', fakeAsync(inject(
    [HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
      let fakeResponse = {status: 200, statusText: 'success'};
      const fakeEmail = 'test@example.org'
      component.alarmForm = {
        controls: {
          email: {
            value: fakeEmail
          },
          phone: {
            value: null
          }
        }
      } as any
      component.createAlert()

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/alarm`,
        method: 'POST'
      });

      requestWrapper.flush({data: {}, status: true, statusText: 'success'}, fakeResponse);
      tick()
      expect(requestWrapper.request.method).toEqual('POST');
      expect(requestWrapper.request.url).toEqual(`${AppConfig.endpoint}/alarm`)
      expect(requestWrapper.request.body).toEqual({email: fakeEmail, phone: null})
  })));

})
