import { Pipe, PipeTransform } from '@angular/core';
import {AppConfig} from "../app.config";

@Pipe({
  name: 'assetUrl'
})
export class AssetUrlPipe implements PipeTransform {


  transform(value: unknown, ...args: unknown[]): unknown {
    return AppConfig.assetEndpoint + value
  }

}
