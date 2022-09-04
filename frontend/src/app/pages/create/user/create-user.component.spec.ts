import {CreateUserComponent} from "./create-user.component";
import {ComponentFixture, fakeAsync, inject, TestBed, tick} from "@angular/core/testing";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {HttpClientTestingModule, HttpTestingController} from "@angular/common/http/testing";
import {MatDialogModule, MatDialogRef} from "@angular/material/dialog";
import {LocalStorageModule} from "angular-2-local-storage";
import {TokenProvider} from "../../../providers/token.provider";
import {AppConfig} from "../../../app.config";

describe('Create Alarm', () => {
  let fixture: ComponentFixture<CreateUserComponent>
  let component: CreateUserComponent;
  beforeEach(() => {

    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
        MatDialogModule,
        LocalStorageModule.forRoot()],
      providers: [TokenProvider, {provide : MatDialogRef, useFactory: () => jasmine.createSpyObj('MatDialogRef', ['close', 'afterClosed']) }],
      declarations: [CreateUserComponent]
    })

    fixture = TestBed.createComponent(CreateUserComponent)
    component = fixture.componentInstance
  })


  it('should create the component', () => {
    expect(component).toBeDefined()
  })

  it('should have markup within the page', () => {
    expect(fixture.nativeElement.innerHTML).toContain('class="text-white font-light ml-[5px]">Done</span>')
  })

  it('should create alert', fakeAsync(inject(
    [HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
      let fakeResponse = {status: 200, statusText: 'success'};
      const fakeEmail = 'test@example.org'
      component.userForm = {
        valid: true,
        pristine: false,
        controls: {
          firstname: {
            value: 'firstnametest'
          },
          lastname: {
            value: 'testUser'
          },
          phone: {
            value: '345232233'
          },
          email: {
            value: 'test@test.org'
          }
        }
      } as any
      component.submitUser()

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/user`,
        method: 'POST'
      });

      requestWrapper.flush({data: {}, status: true, statusText: 'success'}, fakeResponse);
      tick()
      expect(requestWrapper.request.method).toEqual('POST');
      expect(requestWrapper.request.url).toEqual(`${AppConfig.endpoint}/user`)
      expect(requestWrapper.request.body).toBeInstanceOf(FormData)
    })));

})
