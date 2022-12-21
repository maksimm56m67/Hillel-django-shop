import requests



class GetCurrencyBaseClient:
    base_url = None

    def _request(self, method: str,
                 params: dict = None,
                 headers: dict = None,
                 data: dict = None):
        try:
            response = requests.request(
                url=self.base_url,
                method=method,
                params=params or {},
                data=data or {},
                headers=headers or {}
            )
        except Exception:
            # todo logging errors and success results
            ...
        else:
            return response.json()


class PrivatBankAPI(GetCurrencyBaseClient):

    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def get_currency(self):
        currency_list = self._request(
            'GET',
            params={'exchange': '', 'json': '', 'coursid': 5}
        )
        for currency in currency_list:
            if 'err_internal_server_error' in currency.keys() or 'err_incorrect_json' in currency.keys():
                return dict(MonobankAPI())
        return currency_list


class MonobankAPI(GetCurrencyBaseClient):

    _url = 'https://api.monobank.ua/bank/currency'

    def _reformat_currency(self):
        currency_codes = {
            980: 'UAH',
            840: 'USD',
            978: 'EUR'
        }
        
        currency_list = self._request(
            'GET',
            params={'json': ''}
        )

        reform_currency_list = []
        for currency in range(len(currency_list)):
            if currency_codes[currency_list[currency].get('currencyCodeB')] == 'UAH' and currency_list[currency].get('currencyCodeA') in currency_codes.keys():
                reform_currency_list.append({
                    'currencyCodeA': (currency_list[currency].get('currencyCodeA')),
                    'currencyCodeB': (currency_list[currency].get('currencyCodeB')),
                    'buy': (currency_list[currency].get('rateBuy')),
                    'sale': (currency_list[currency].get('rateSell'))
                    })
        return reform_currency_list
    


privat_currency_client = PrivatBankAPI()

