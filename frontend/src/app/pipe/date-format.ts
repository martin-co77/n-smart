import { Pipe, PipeTransform } from '@angular/core';
import {DatePipe} from "@angular/common";

@Pipe({
  name: 'dateFormat'
})
export class DateFormat extends DatePipe implements PipeTransform {

  transform(value: any, ...arg: any[]): any {
    return super.transform(value, 'dd-MM-yyyy H:m')
  }

}
