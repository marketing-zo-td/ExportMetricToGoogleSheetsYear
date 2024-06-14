import os

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from gspread import service_account

from api_util import get_log_data
from api_fields import visit_field_list


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    counter_id = os.getenv("COUNTER_ID")
    api_host_url = "https://api-metrika.yandex.ru"

#    start_date = os.getenv("START_DATE")
    start_date = (date.today() - relativedelta(days=406)).strftime("%Y-%m-%d")
    yesterday = (date.today() - relativedelta(days=336)).strftime("%Y-%m-%d")
    end_date = os.getenv("END_DATE", default=yesterday)

    data_list = [{
        "source": "visits",
        "api_field_list": visit_field_list,
        "google_sheet_url": os.getenv("VISIT_SHEET_URL")
    }]
    gc = service_account()

    for data_elem in data_list:
        data = get_log_data(api_host_url,
                            counter_id,
                            token,
                            data_elem["source"],
                            start_date,
                            end_date,
                            data_elem["api_field_list"])

        sh = gc.open_by_url(data_elem["google_sheet_url"])
        sh.sheet1.update([data.columns.values.tolist()]
                         + data.fillna("Unknown").values.tolist())
