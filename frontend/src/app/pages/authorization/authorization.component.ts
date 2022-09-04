import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {AppConfig} from "../../app.config";
import {TokenProvider} from "../../providers/token.provider";
import {Router} from "@angular/router";
import {ImageCaptureProvider} from "../../providers/imageCapture.provider";

@Component({
  selector: 'app-authorization',
  templateUrl: './authorization.component.html',
  styleUrls: ['./authorization.component.scss']
})
export class AuthorizationComponent implements OnInit {
  @ViewChild('authImage', {static: false}) authImage: ElementRef<HTMLImageElement>

  /**
   * @param http
   * @param tokenProvider
   * @param router
   * @param imageCaptureProvider
   */
  constructor(
    private http: HttpClient,
    private tokenProvider: TokenProvider,
    private router: Router,
    private imageCaptureProvider: ImageCaptureProvider
  ) { }

  ngOnInit(): void {}

  authorize() {
    navigator.mediaDevices.getUserMedia({video: true})
      .then((stream) => {
        this.imageCaptureProvider.buildVideo(stream).then((blob) => {
          this.authImage.nativeElement.src = URL.createObjectURL(blob as any);
          this.sendForAuthorization(blob as any);
        })
      });
  }

  /**
   * @param blob
   */
  sendForAuthorization(blob: Blob) {
    const formData = new FormData();
    formData.append('photo', blob);
    const subscription = this.http.post(`${AppConfig.endpoint}/auth`, formData).subscribe((r: any) => {
      if (r.status && r.status_text) {
        const data = r.data
        this.tokenProvider.save(data.token, {
          id: data.id,
          firstname: data.firstname,
          lastname: data.lastname,
          picture: data.picture,
          lastLogin: data.last_login,
          is_super: data.is_super
        });
        this.router.navigate(['/dashboard']).then(() => {
          window.location.reload()
        })
      }
    }, ()=> {
      window.alert('Authorization failed. Please try again!')
    });

    subscription.add(() => {
      subscription.unsubscribe()
    })
  }
}
