import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {WebhookComponent} from "./pages/webhook/webhook.component";
import {SidebarComponent} from "./pages/sidebar/sidebar.component";
import {AuthorizationComponent} from "./pages/authorization/authorization.component";
import {AlarmComponent} from "./pages/alarm/alarm.component";
import {UserComponent} from "./pages/user/user.component";
import {DashboardComponent} from "./pages/dashboard/dashboard.component";
import {DataTablesModule} from "angular-datatables";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatDialogModule} from '@angular/material/dialog';
import {HttpClientModule} from "@angular/common/http";
import {TokenProvider} from "./providers/token.provider";
import {LocalStorageModule} from "angular-2-local-storage";
import {CreateUserComponent} from "./pages/create/user/create-user.component";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {IntruderAlertComponent} from "./pages/create/intruder-alert/intruder-alert.component";
import {CreateWebHookComponent} from "./pages/create/webhook/create-webhook.component";
import {UserAvatarComponent} from "./pages/create/user-avatar/user-avatar.component";
import {DateFormat} from "./pipe/date-format";
import {AssetUrlPipe} from "./pipe/asset-url.pipe";


@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    UserComponent,
    AlarmComponent,
    WebhookComponent,
    SidebarComponent,
    AuthorizationComponent,
    IntruderAlertComponent,
    CreateUserComponent,
    DateFormat,
    CreateWebHookComponent,
    UserAvatarComponent,
    AssetUrlPipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    DataTablesModule,
    MatDialogModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    HttpClientModule,
    LocalStorageModule.forRoot()
  ],
  providers: [TokenProvider],
  bootstrap: [AppComponent]
})
export class AppModule { }
