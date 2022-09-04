import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {TokenProvider} from "../../providers/token.provider";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AppConfig} from "../../app.config";
import {MatDialog} from "@angular/material/dialog";
import {UserAvatarComponent} from "../create/user-avatar/user-avatar.component";


declare var webkitSpeechRecognition: any;
declare var webkitSpeechGrammarList: any;

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  private _dashStats: any = {} as any
  private speechRecognition: any = {} as any;
  private speechTimeout: any = {} as any;
  constructor(
    private tokenProvider: TokenProvider,
    private http: HttpClient,
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.loadDashboard();
    this.initSpeech();
  }

  speechRecogHandler(): any {
    return new webkitSpeechRecognition();
  }

  initSpeech() {
    this.speechRecognition = this.speechRecogHandler()
    this.speechRecognition.continous = false;
    this.speechRecognition.lang = 'en-US';
    this.speechRecognition.interimResults = true;
    this.speechRecognition.maxAlternatives = 1;
    this.speechRecognition.onresult = (event: any) => {
      clearTimeout(this.speechTimeout)
      this.speechTimeout = setTimeout(() => {
        this.speechRecognition.stop();
        this.onSpeechResult(event.results[0][0].transcript);
      }, 2000);
    }
  }

  onSpeechResult(result: string) {
    if (confirm(`This speech command will trigger the webhook for "${result}". Do you want to continue`)) {
      const headers = new HttpHeaders({Authorization: this.tokenProvider.getToken()})
      const subscription = this.http.post(`${AppConfig.endpoint}/webhook/incoming`,
        {event: 'speech', data: result}, {
        headers: headers
      }).pipe().subscribe({
        next: (res: any) => {
          if (res.data) {
            this.loadDashboard();
            alert('Speech command sent successfully!');
          }
        },
        error: (e) => console.error(e)
      })
      subscription.add(() => subscription.unsubscribe());

    }
  }

  loadDashboard() {
    const headers = new HttpHeaders({Authorization: `Bearer ${this.tokenProvider.getToken()}`})
    const subscription = this.http.get(`${AppConfig.endpoint}/stat`, {
      headers: headers
    }).pipe().subscribe({
      next: (res: any) => {
        if (res.data) {
          this._dashStats = res.data;
          const grammar = `#JSGF V1.0; grammar grammars; public <grammar> = ${this._dashStats.grammar.join(' | ')};`
          const speechRecognitionList = new webkitSpeechGrammarList();
          speechRecognitionList.addFromString(grammar, 1);
          this.speechRecognition.grammars = speechRecognitionList;
        }
      },
      error: (e) => console.error(e)
    });

    subscription.add(() => subscription.unsubscribe());
  }

  get dashStat(): any {
    return this._dashStats;
  }

  change_image() {

  }

  recognize_speech() {
    this.speechRecognition.start();
  }

  changeUserImage() {
    this.dialog.open(UserAvatarComponent, {})
  }

}
