import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {TokenProvider} from "../../../providers/token.provider";
import {MatDialogRef} from "@angular/material/dialog";
import {AppConfig} from "../../../app.config";

@Component({
  selector: 'app-webhook',
  templateUrl: './create-webhook.component.html',
  styleUrls: ['./create-webhook.component.scss']
})
export class CreateWebHookComponent implements OnInit {

  public deviceForm: FormGroup = new FormGroup({
    'type': new FormControl('authorize', [Validators.required]),
    'name': new FormControl('', [Validators.required]),
    'url': new FormControl('', [Validators.required])
  })
  constructor(
    private http: HttpClient,
    private tokenProvider: TokenProvider,
    private dialogRef: MatDialogRef<any>
  ) { }

  ngOnInit(): void {
  }

  createDevice() {
    const headers = new HttpHeaders({Authorization: 'Bearer ' + this.tokenProvider.getToken()})
    const subscription = this.http.post(`${AppConfig.endpoint}/webhook`,
      {
        event: this.deviceForm.controls['type'].value,
        name: this.deviceForm.controls['name'].value,
        url: this.deviceForm.controls['url'].value
      },{
        headers: headers
      }).pipe().subscribe({
      next: (res: any) => {
        if (res.data) {
          alert('Webhook created successfully')
          this.dialogRef.close();
        }
      },
      error: (e) => console.error(e)
    });
    subscription.add(() => subscription.unsubscribe())
  }


}
