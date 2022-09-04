import {Component, OnInit, ViewChild} from '@angular/core';
import {MatDialog} from "@angular/material/dialog";
import {Subject} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {TokenProvider} from "../../providers/token.provider";
import {AppConfig} from "../../app.config";
import {CreateWebHookComponent} from "../create/webhook/create-webhook.component";
import {DataTableDirective} from "angular-datatables";
import {TableHelper} from "../../providers/table.helper";

@Component({
  selector: 'app-webhook',
  templateUrl: './webhook.component.html',
  styleUrls: ['./webhook.component.scss']
})
export class WebhookComponent implements OnInit {
  @ViewChild(DataTableDirective, {static: false})
  dtElement: DataTableDirective;
  private _webhooks = []
  public dtOptions: DataTables.Settings = {}
  public dtTrigger: Subject<any> = new Subject<any>()
  private dtHelper: TableHelper
  constructor(
    private http: HttpClient,
    private tokenProvider: TokenProvider,
    public dialog: MatDialog
  ) {
  }

  ngOnInit(): void {
    this.loadWebhook();
  }

  ngAfterViewInit() {
    this.dtHelper = new TableHelper(this.dtElement)
  }


  loadWebhook() {
    const headers = new HttpHeaders({Authorization: 'Bearer ' + this.tokenProvider.getToken()})
    const subscription = this.http.get(`${AppConfig.endpoint}/webhook`, {
      headers: headers
    }).pipe().subscribe({
      next: (res: any) => {
        if (res.data) {
          this._webhooks = Array.isArray(res.data) ? res.data: []
          if (this._webhooks.length) {
            this.dtHelper.reInitDataTable(() => {
              this.dtTrigger.next(this._webhooks)
            })
          }
        }
      },
      error: (e) => console.error(e)
    });
    subscription.add(() => subscription.unsubscribe())
  }

  get webhooks(): Array<any> {
    return this._webhooks
  }

  ngOnDestroy() {
    this.dtTrigger.unsubscribe();
  }


  deleteWebHook(id: number) {
    const headers = new HttpHeaders({Authorization: 'Bearer ' + this.tokenProvider.getToken()})
    const subscription = this.http.delete(`${AppConfig.endpoint}/webhook/${id}`, {
      headers: headers
    }).pipe().subscribe({
      next: (res: any) => {
        if (res.data) {
          this.loadWebhook();
          alert('Deleted successfully!')
        }
      },
      error: (e) => console.error(e)
    });
    subscription.add(() => subscription.unsubscribe())
  }

  addWebHook() {
    const subscription = this.dialog.open(CreateWebHookComponent, {}).afterClosed().subscribe(() => this.loadWebhook())

    subscription.add(() => subscription.unsubscribe())
  }

  get isSuper(): boolean {
    return this.tokenProvider.isSuper()
  }
}
