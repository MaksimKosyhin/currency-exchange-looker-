from io import StringIO

import gspread
import pandas as pd
import sys

data = pd.read_json(StringIO(sys.argv[1]))
data = data[['exchangedate', 'rate_per_unit']].iloc[::-1]

gc = gspread.service_account(filename='service-account.json')
sh = gc.open('currency exchange (USD)')

worksheet = sh.sheet1
worksheet.batch_clear(['A:A', 'B:B'])
worksheet.update([data.columns.values.tolist()] + data.values.tolist())
