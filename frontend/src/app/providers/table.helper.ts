import {DataTableDirective} from "angular-datatables";

export class TableHelper {
  private dtInit = false;
  constructor(private dtElement: DataTableDirective) {
  }

  public reInitDataTable(callback = () => {}) {
    if (this.dtInit) {
      this.dtElement.dtInstance.then((dtInstance: DataTables.Api) => {
        dtInstance.destroy()
        callback()
      })
    } else {
      this.dtInit = true;
      callback()
    }
  }
}
