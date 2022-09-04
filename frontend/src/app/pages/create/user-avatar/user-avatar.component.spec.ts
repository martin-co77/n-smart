import {ComponentFixture, fakeAsync, inject, TestBed, tick} from "@angular/core/testing";
import {UserAvatarComponent} from "./user-avatar.component";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {HttpClientTestingModule, HttpTestingController} from "@angular/common/http/testing";
import {MatDialogModule, MatDialogRef} from "@angular/material/dialog";
import {LocalStorageModule} from "angular-2-local-storage";
import {TokenProvider} from "../../../providers/token.provider";
import {ImageCaptureProvider} from "../../../providers/imageCapture.provider";
import {AppConfig} from "../../../app.config";

describe('Update avatar', () => {
  let fixture: ComponentFixture<UserAvatarComponent>
  let component: UserAvatarComponent

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
        MatDialogModule,
        LocalStorageModule.forRoot()],
      providers: [TokenProvider, {provide : MatDialogRef, useFactory: () => jasmine.createSpyObj('MatDialogRef', ['close', 'afterClosed']) }],
      declarations: [UserAvatarComponent]
    })

    fixture = TestBed.createComponent(UserAvatarComponent)
    component = fixture.componentInstance
  })

  it('should create the component', () => {
    expect(component).toBeDefined()
  })

  it('should have elements within the page', () => {
    expect(fixture.nativeElement.innerHTML).toContain(' class="text-white font-light ml-[5px]">Submit</span>')
  })

  it('should produce a blob and send it for avatar', fakeAsync(inject(
    [ImageCaptureProvider],(imageCaptureProvider: ImageCaptureProvider)=> {
      const avatarImageSpy = jasmine.createSpyObj('ElementRef<HTMLImageElement>', {nativeElement: {src: null}})
      component.userAvatar = avatarImageSpy
      const fakeBlobUrlSpy = jasmine.createSpy().and.returnValue('test url')
      URL.createObjectURL = fakeBlobUrlSpy
      const fakeStream = jasmine.createSpy()
      const fakeBlob = new Blob([])
      const fakeMediaDevices = jasmine.createSpy().and.resolveTo(fakeStream)
      const buildVideo = spyOn(imageCaptureProvider, 'buildVideo').and.resolveTo(fakeBlob as any)
      navigator.mediaDevices.getUserMedia = fakeMediaDevices;
      component.captureUser()
      tick()
      expect(fakeMediaDevices).toHaveBeenCalledTimes(1)
      expect(buildVideo).toHaveBeenCalled()
      expect(avatarImageSpy.nativeElement.src).toEqual('test url')
      expect(fakeBlobUrlSpy).toHaveBeenCalledOnceWith(fakeBlob as any)
    })))


  it('should submit avatar to the server for further processing', fakeAsync(inject(
    [HttpClient, HttpTestingController, TokenProvider],
    (http: HttpClient, backend: HttpTestingController, tokenProvider: TokenProvider) => {
      const tokenProviderUserDataSpy = spyOn(tokenProvider, 'getUserData').and.returnValue({
        id: 1
      } as any)
      component.userImage = {
        size: 10
      } as any;
      let fakeResponse = {status: 201, statusText: 'success'};
      component.changePicture()

      const requestWrapper = backend.expectOne({
        url: `${AppConfig.endpoint}/user/1`,
        method: 'PUT'
      });

      requestWrapper.flush({data: {}, status: true, statusText: 'success'}, fakeResponse);
      tick()
      expect(requestWrapper.request.method).toEqual('PUT');
      expect(requestWrapper.request.body).toBeInstanceOf(FormData)
      expect(tokenProviderUserDataSpy).toHaveBeenCalledTimes(1);
    })))
})
