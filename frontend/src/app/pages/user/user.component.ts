import {AfterViewInit, Component, ElementRef, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AppConfig} from "../../app.config";
import {TokenProvider} from "../../providers/token.provider";
import {Subject} from "rxjs";
import {CreateUserComponent} from "../create/user/create-user.component";
import {MatDialog} from "@angular/material/dialog";
import {DataTableDirective} from "angular-datatables";
import {TableHelper} from "../../providers/table.helper";

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
export class UserComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild(DataTableDirective, {static: false})
  dtElement: DataTableDirective;
  private _users = []
  public dtOptions: DataTables.Settings = {}
  public dtTrigger: Subject<any> = new Subject<any>()
  private dtHelper: TableHelper
  constructor(
    private http: HttpClient,
    private tokenProvider: TokenProvider,
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.loadUsers();
  }

  ngAfterViewInit() {
    this.dtHelper = new TableHelper(this.dtElement)
  }

  loadUsers() {
    const headers = new HttpHeaders({Authorization: 'Bearer ' + this.tokenProvider.getToken()})
    const subscription = this.http.get(`${AppConfig.endpoint}/user`, {
      headers: headers
    }).pipe().subscribe({
      next: (res: any) => {
        if (res.data) {
          this._users = Array.isArray(res.data) ? res.data: []
          if (this._users.length) {
            this.dtHelper.reInitDataTable(() => {
              this.dtTrigger.next(this._users)
            })
          }
        }
      },
      error: (e) => console.error(e)
    });
    subscription.add(() => subscription.unsubscribe())
  }

  get users(): Array<any> {
    return this._users
  }

  addUser() {
    const subscription = this.dialog.open(CreateUserComponent, {}).afterClosed().subscribe(() => this.loadUsers())
    subscription.add(() => subscription.unsubscribe())
  }

  deleteUser(id: number) {
    const headers = new HttpHeaders({Authorization: 'Bearer ' + this.tokenProvider.getToken()})
    const subscription = this.http.delete(`${AppConfig.endpoint}/user/${id}`, {
      headers: headers
    }).pipe().subscribe({
      next: (res: any) => {
        if (res.data) {
          this.loadUsers();
          alert('Deleted successfully!')
        }
      },
      error: (e) => console.error(e)
    });
    subscription.add(() => subscription.unsubscribe())
  }

  ngOnDestroy() {
    this.dtTrigger.unsubscribe();
  }

  get isSuper(): boolean {
    return this.tokenProvider.isSuper()
  }

}
