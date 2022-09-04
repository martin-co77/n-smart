import {UserComponent} from "./user.component";
import {ComponentFixture, fakeAsync, inject, TestBed, tick} from "@angular/core/testing";
import {TokenProvider} from "../../providers/token.provider";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {HttpClientTestingModule, HttpTestingController} from "@angular/common/http/testing";
import {LocalStorageModule} from "angular-2-local-storage";
import {MatDialogModule} from "@angular/material/dialog";
import {AppConfig} from "../../app.config";


describe('Webhook component', () => {
  let component: UserComponent;
  let fixture: ComponentFixture<UserComponent>;
  let table: HTMLElement;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [UserComponent],
      providers: [TokenProvider],
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
        LocalStorageModule.forRoot(),
        MatDialogModule
      ]
    });
    fixture = TestBed.createComponent(UserComponent);
    component = fixture.componentInstance;
    table = fixture.nativeElement.querySelector('table');
  });

  it('should create the component', () => {
    expect(component).toBeDefined()
  })

  it('should have table within the page', () => {
    expect(table.innerHTML).toContain('Name')
  })

  it('should issue a request to fetch alerts', fakeAsync(inject(
    [HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
      let fakeResponse = {status: 200, statusText: 'success'};
      component.loadUsers()

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/user`,
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
      component.deleteUser(1)

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/user/1`,
        method: 'DELETE'
      });

      requestWrapper.flush({data: [], status: true, statusText: 'success'}, fakeResponse);
      tick()
      expect(requestWrapper.request.method).toEqual('DELETE');
    })))
})

