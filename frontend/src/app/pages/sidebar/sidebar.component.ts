import { Component, OnInit } from '@angular/core';
import {TokenProvider, UserDataInterface} from "../../providers/token.provider";

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  private _userdata: UserDataInterface = {} as any;
  constructor(private tokenProvider: TokenProvider) { }

  ngOnInit(): void {
    this._userdata = this.tokenProvider.getUserData()
  }


  get userdata(): UserDataInterface {
    return this._userdata
  }
}
