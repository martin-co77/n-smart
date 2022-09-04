import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {ImageCaptureProvider} from "../../../providers/imageCapture.provider";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AppConfig} from "../../../app.config";
import {TokenProvider} from "../../../providers/token.provider";
import {MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-user-avatar',
  templateUrl: './user-avatar.component.html',
  styleUrls: ['./user-avatar.component.scss']
})
export class UserAvatarComponent implements OnInit {
  @ViewChild('userAvatar', {static: false}) userAvatar: ElementRef<any>;
  public userImage: Blob = {} as any
  constructor(
    private imageCaptureProvider: ImageCaptureProvider,
    private tokenProvider: TokenProvider,
    private dialogRef: MatDialogRef<any>,
    private http: HttpClient
  ) { }

  ngOnInit(): void {}

  captureUser() {
    navigator.mediaDevices.getUserMedia({video: true})
      .then((stream) => {
        this.imageCaptureProvider.buildVideo(stream).then((blob: any) => {
          this.userAvatar.nativeElement.src = URL.createObjectURL(blob as any);
          this.userImage = blob;
        })
      });
  }

  changePicture() {
    if (!this.userImage.size) {
      return alert('Please capture image to continue!')
    }

    const formData = new FormData()
    formData.append('photo', this.userImage)

    const headers = new HttpHeaders({Authorization: 'Bearer ' + this.tokenProvider.getToken()})
    const subscription = this.http.put(
      `${AppConfig.endpoint}/user/${this.tokenProvider.getUserData().id}`,
      formData,
      {
      headers: headers
    }).subscribe({
      next: (res: any) => {
        if (res.data) {
          alert('User image updated successfully!')
          this.dialogRef.close();
        }
      },
      error: (e) => console.error(e)
    });
    subscription.add(() => subscription.unsubscribe())
  }
}
