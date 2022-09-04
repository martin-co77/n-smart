import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {SidebarComponent} from "./pages/sidebar/sidebar.component";
import {AuthorizationComponent} from "./pages/authorization/authorization.component";
import {DashboardComponent} from "./pages/dashboard/dashboard.component";
import {UserComponent} from "./pages/user/user.component";
import {AlarmComponent} from "./pages/alarm/alarm.component";
import {WebhookComponent} from "./pages/webhook/webhook.component";
import {AuthGuard} from "./providers/authguard";

const routes: Routes = [
  {
    path: '',
    component: AuthorizationComponent
  }, {
    path: 'dashboard',
    component: SidebarComponent,
    canActivate: [AuthGuard],
    children: [
        {
          path: '',
          component: DashboardComponent,
          canActivate: [AuthGuard],
        },
        {
          path: 'home',
          component: DashboardComponent,
          canActivate: [AuthGuard]
        }, {
          path: 'user',
          component: UserComponent,
          canActivate: [AuthGuard]
        }, {
          path: 'alarm',
          component: AlarmComponent,
          canActivate: [AuthGuard]
        }, {
          path: 'device',
          component: WebhookComponent,
          canActivate: [AuthGuard]
        }
      ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
