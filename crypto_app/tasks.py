import json
from datetime import datetime

import requests
from celery import shared_task

from .models import Crypto


@shared_task()
def db_filling():
    cpcurr_code = {'BTC': 189, 'BCH': 215, 'ETH': 195, 'DASH': 199, 'LTC': 191, 'XRP': 197}
    curr_code = {'UAH': 85, 'USD': 12, 'EUR': 17, 'GBP': 3}

    now = datetime.now().isoformat(' ', 'minutes')
    dat = datetime.strptime(now, "%Y-%m-%d %H:%M")

    for key in cpcurr_code.items():
        for elem in curr_code.items():
            url = f'https://ru.investing.com/currencyconverter/service/RunConvert?fromCurrency={key[1]}&toCurrency={elem[1]}&fromAmount=1&toAmount=39170&currencyType=1'
            response = requests.get(url=url, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
                'X-Requested-With': 'XMLHttpRequest'})
            res = json.loads(response.text)
            resulttmp = res.get('calculatedAmount')
            result = float(resulttmp.replace(',', '.'))
            Crypto(time_create=dat, cp_curr=key[0], curr=elem[0], price=result).save()
