import {ComponentFixture, fakeAsync, inject, TestBed, tick} from "@angular/core/testing";
import {AuthorizationComponent} from "./authorization.component";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {HttpClientTestingModule, HttpTestingController} from "@angular/common/http/testing";
import {TokenProvider} from "../../providers/token.provider";
import {RouterModule} from "@angular/router";
import {ImageCaptureProvider} from "../../providers/imageCapture.provider";
import {LocalStorageModule} from "angular-2-local-storage";
import {AppConfig} from "../../app.config";

describe('Verify the authorization component', () => {
  let component: AuthorizationComponent
  let fixture: ComponentFixture<AuthorizationComponent>
  let submissionButton: HTMLButtonElement
  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AuthorizationComponent],
      imports: [HttpClientModule, HttpClientTestingModule, RouterModule, LocalStorageModule.forRoot()],
      providers: [TokenProvider, ImageCaptureProvider]
    })

    fixture = TestBed.createComponent(AuthorizationComponent)
    component = fixture.componentInstance;
    submissionButton = fixture.nativeElement.querySelector('button')
  })

  it('should verify that component is created', () => {
    expect(component).toBeDefined()
  })

  it('should produce a blob and send it for verification', fakeAsync(inject(
    [ImageCaptureProvider],(imageCaptureProvider: ImageCaptureProvider)=> {
      const authImageSpy = jasmine.createSpyObj('ElementRef<HTMLImageElement>', {nativeElement: {src: null}})
      component.authImage = authImageSpy
      const fakeSendForAuthorization = spyOn(component, 'sendForAuthorization')
      const fakeBlobUrlSpy = jasmine.createSpy().and.returnValue('test url')
      URL.createObjectURL = fakeBlobUrlSpy
      const fakeStream = jasmine.createSpy()
      const fakeBlob = new Blob([])
      const fakeMediaDevices = jasmine.createSpy().and.resolveTo(fakeStream)
      const buildVideo = spyOn(imageCaptureProvider, 'buildVideo').and.resolveTo(fakeBlob as any)
      navigator.mediaDevices.getUserMedia = fakeMediaDevices;
      component.authorize()
      tick()
      expect(fakeMediaDevices).toHaveBeenCalledTimes(1)
      expect(buildVideo).toHaveBeenCalled()
      expect(fakeSendForAuthorization).toHaveBeenCalledOnceWith(fakeBlob as any)
      expect(authImageSpy.nativeElement.src).toEqual('test url')
      expect(fakeBlobUrlSpy).toHaveBeenCalledOnceWith(fakeBlob as any)
    })))


  it('should try authorizing using fake blob', fakeAsync(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {
    let fakeResponse = {status: 201, statusText: 'success'};
    component.sendForAuthorization(new Blob([]))

    const requestWrapper = backend.expectOne({
      url: `${AppConfig.endpoint}/auth`,
      method: 'POST'
    });

    requestWrapper.flush(
      {
        data: {
          id: 1,
          firstname: 'test',
          lastname: 'testPerson',
          picture: 'http://test.jpg',
          lastLogin: '2022-08-23 04:33:22',
          is_super: 1
      },
      status: true, statusText: 'success'}, fakeResponse);
    tick()
    expect(requestWrapper.request.method).toEqual('POST');
  })))
})
