import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {ImageCaptureProvider} from "../../../providers/imageCapture.provider";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AppConfig} from "../../../app.config";
import {TokenProvider} from "../../../providers/token.provider";
import {MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-create-user',
  templateUrl: './create-user.component.html',
  styleUrls: ['./create-user.component.scss']
})
export class CreateUserComponent implements OnInit {
  @ViewChild('userAvatar', {static: false}) userAvatar: ElementRef<any>;
  private userImage: Blob;

  public userForm: FormGroup = new FormGroup({
    firstname: new FormControl('', [Validators.required]),
    lastname: new FormControl('', [Validators.required]),
    phone: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required])
  })

  constructor(
    private imageCaptureProvider: ImageCaptureProvider,
    private http: HttpClient,
    private tokenProvider: TokenProvider,
    private dialogRef: MatDialogRef<any>
  ) { }

  ngOnInit(): void {
  }

  submitUser() {
    if (!this.userForm.valid || this.userForm.pristine) {
      return alert('All fields are required');
    }

    const formData = new FormData()
    formData.append('firstname', this.userForm.controls['firstname'].value);
    formData.append('lastname', this.userForm.controls['lastname'].value);
    formData.append('phone', this.userForm.controls['phone'].value);
    formData.append('email', this.userForm.controls['email'].value);
    formData.append('photo', this.userImage)

    const headers = new HttpHeaders({Authorization: 'Bearer ' + this.tokenProvider.getToken()})
    const subscription = this.http.post(`${AppConfig.endpoint}/user`, formData, {
      headers: headers
    }).subscribe({
      next: (res: any) => {
        if (res.data) {
          alert('User created successfully!')
          this.dialogRef.close();
        }
      },
      error: (e) => console.error(e)
    });
    subscription.add(() => subscription.unsubscribe())
  }

  captureUser() {
    navigator.mediaDevices.getUserMedia({video: true})
      .then((stream) => {
        this.imageCaptureProvider.buildVideo(stream).then((blob: any) => {
          this.userAvatar.nativeElement.src = URL.createObjectURL(blob as any);
          this.userImage = blob;
        })
      });
  }
}
