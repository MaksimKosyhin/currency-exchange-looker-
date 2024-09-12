from io import StringIO

import gspread
import pandas as pd
import sys

import requests

update_from = sys.argv[1]
update_to = sys.argv[2]

url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={update_from}&end={update_to}&valcode=usd&sort=exchangedate&order=desc&json'
response = requests.get(url)

data = pd.read_json(StringIO(response.text))
data = data[['exchangedate', 'rate_per_unit']].iloc[::-1]

gc = gspread.service_account(filename='service-account.json')
sh = gc.open('currency exchange (USD)')

worksheet = sh.sheet1
worksheet.batch_clear(['A:A', 'B:B'])
worksheet.update([data.columns.values.tolist()] + data.values.tolist())
