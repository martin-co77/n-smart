import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AppConfig} from "../../../app.config";
import {TokenProvider} from "../../../providers/token.provider";
import {MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-intruder-alert',
  templateUrl: './intruder-alert.component.html',
  styleUrls: ['./intruder-alert.component.scss']
})
export class IntruderAlertComponent implements OnInit {
  public alarmForm: FormGroup = new FormGroup({
    'email': new FormControl(null, [Validators.required]),
    'phone': new FormControl(null, [Validators.required])
  })
  constructor(
    private http: HttpClient,
    private tokenProvider: TokenProvider,
    private dialogRef: MatDialogRef<any>
  ) { }

  ngOnInit(): void {
  }

  createAlert() {
    const headers = new HttpHeaders({Authorization: 'Bearer ' + this.tokenProvider.getToken()})
    const subscription = this.http.post(`${AppConfig.endpoint}/alarm`,
      {
        email: this.alarmForm.controls['email'].value,
        phone: this.alarmForm.controls['phone'].value
      },{
      headers: headers
    }).pipe().subscribe({
      next: (res: any) => {
        if (res.data) {
          alert('Notification created successfully')
          this.dialogRef.close();
        }
      },
      error: (e) => console.error(e)
    });
    subscription.add(() => subscription.unsubscribe())
  }

}
