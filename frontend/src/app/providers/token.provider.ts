import {Injectable} from "@angular/core";
import {LocalStorageService} from "angular-2-local-storage";

export interface UserDataInterface {
  id: number;
  firstname: string;
  lastname: string;
  picture: string;
  lastLogin: string;
  is_super: boolean;
}

@Injectable()
export class TokenProvider {
  tokenKey = 'authToken';
  tokenTime = 'authTokenTime';
  userDataKey = 'userData'

  constructor(private localStorage: LocalStorageService) {}


  save(token: string, data: any) {
    this.localStorage.set(this.tokenKey, token);
    this.localStorage.set(this.tokenTime, (new Date()).getTime());
    this.localStorage.set(this.userDataKey, data);
  }

  canReAuthenticate(): boolean {
    const lastStoredTokenDate = (new Date(this.localStorage.get(this.tokenTime))).getTime();
    const currentDate = (new Date()).getTime()
    return (currentDate - lastStoredTokenDate) > (60 * 60 * 60) * 1000;
  }

  getToken(): string {
    return this.localStorage.get(this.tokenKey);
  }

  getUserData(): UserDataInterface {
    return this.localStorage.get(this.userDataKey) || {} as any;
  }

  isSuper() {
    return this.getUserData().is_super
  }

}
