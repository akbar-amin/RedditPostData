import os 
import dotenv
import gspread
import pandas as pd 
from pathlib import Path
from gspread.auth import DEFAULT_SERVICE_ACCOUNT_FILENAME
from gspread.exceptions import APIError
from gspread.models import Worksheet

from .utils import transform 

__all__ = ["Sheets"]

dotenv.load_dotenv(dotenv.find_dotenv())

class Sheets:
    def __init__(self, spreadsheet: str = None, worksheet: str = None, credentials: Path = None) -> None:
        filename = credentials or os.getenv("CREDENTIALS") or DEFAULT_SERVICE_ACCOUNT_FILENAME
        self.gc = gspread.service_account(filename = filename)
        self.sh = self.gc.open(spreadsheet or os.getenv("SPREADSHEET"))

        if worksheet:
            self.ws = self.sh.worksheet(worksheet) 
        else:
            self.ws = self.sh.get_worksheet(0)

    def worksheets(self)  -> list:
        return self.sh.worksheets()

    def context(self, worksheet: str) -> Worksheet:
        self.ws = self.sh.worksheet(worksheet) 
        return self.ws 

    def new(self, title: str, dims: tuple = (100, 20)) -> Worksheet:
        try:
            self.sh.add_worksheet(title, *dims) 
        except APIError as e:
            if e.response.status_code == 400:
                print(f"{title} already exists and will be overwritten")
            else:
                raise e  
        return self.context(title)

    def load(self, worksheet: str) -> pd.DataFrame:
        return pd.DataFrame(self.context(worksheet).get_all_records())

    def write(self, data: pd.DataFrame, worksheet: str = None, formatting: bool = True) -> None:
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)

        if formatting:
            data = transform(data)

        if worksheet:
            self.ws = self.context(worksheet)

        self.ws.update([data.columns.values.tolist()] + data.values.tolist())
    


