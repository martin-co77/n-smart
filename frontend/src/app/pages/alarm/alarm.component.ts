import {Component, OnInit, ViewChild} from '@angular/core';
import {Subject} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {TokenProvider} from "../../providers/token.provider";
import {AppConfig} from "../../app.config";
import {MatDialog} from "@angular/material/dialog";
import {IntruderAlertComponent} from "../create/intruder-alert/intruder-alert.component";
import {DataTableDirective} from "angular-datatables";
import {TableHelper} from "../../providers/table.helper";

@Component({
  selector: 'app-alarm',
  templateUrl: './alarm.component.html',
  styleUrls: ['./alarm.component.scss']
})
export class AlarmComponent implements OnInit {
  @ViewChild(DataTableDirective, {static: false})
  dtElement: DataTableDirective;
  private _alerts: Array<any> = [];
  public dtOptions: DataTables.Settings = {}
  public dtTrigger: Subject<any> = new Subject<any>()
  private dtHelper: TableHelper
  constructor(
    private http: HttpClient,
    private tokenProvider: TokenProvider,
    private matDialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.loadAlerts();
  }

  ngAfterViewInit() {
    this.dtHelper = new TableHelper(this.dtElement)
  }

  loadAlerts() {
    const headers = new HttpHeaders({Authorization: 'Bearer ' + this.tokenProvider.getToken()})
    const subscription = this.http.get(`${AppConfig.endpoint}/alarm`, {
      headers: headers
    }).pipe().subscribe({
      next: (res: any) => {
        if (res.data) {
          this._alerts = Array.isArray(res.data) ? res.data: []
          if (this._alerts.length) {
            this.dtHelper.reInitDataTable(() => {
              this.dtTrigger.next(this._alerts)
            })
          }
        }
      },
      error: (e) => console.error(e)
    });
    subscription.add(() => subscription.unsubscribe())
  }

  createAlarm() {
    const subscription = this.matDialog.open(IntruderAlertComponent, {}).afterClosed().subscribe(() => this.loadAlerts())
    subscription.add(() => subscription.unsubscribe())
  }

  get alerts(): Array<any> {
    return this._alerts
  }

  ngOnDestroy() {
    this.dtTrigger.unsubscribe();
  }


  deleteAlarm(id: number) {
    const headers = new HttpHeaders({Authorization: 'Bearer ' + this.tokenProvider.getToken()})
    const subscription = this.http.delete(`${AppConfig.endpoint}/alarm/${id}`, {
      headers: headers
    }).pipe().subscribe({
      next: (res: any) => {
        if (res.data) {
          this.loadAlerts();
          alert('Deleted successfully!')
        }
      },
      error: (e) => console.error(e)
    });
    subscription.add(() => subscription.unsubscribe())
  }

  get isSuper(): boolean {
    return this.tokenProvider.isSuper();
  }

}
