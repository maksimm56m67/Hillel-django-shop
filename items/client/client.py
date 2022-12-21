import logging

from bs4 import BeautifulSoup

from shop.api_clients import BaseClient

logger = logging.getLogger(__name__)


class Parser(BaseClient):
    # base_url = 'https://www.olx.ua/d/uk/transport/legkovye-avtomobili/'
    base_url= 'https://www.olx.ua/d/uk/hobbi-otdyh-i-sport/muzykalnye-instrumenty/'

    def parse(self) -> list:
        response = self.get_request(
            method='get',
        )
        soup = BeautifulSoup(response, "html.parser")
        try:
            category_name = soup.find('div', attrs={'data-cy': 'category-dropdown'}).find('div').text
        except (AssertionError, IndexError) as err:
            logger.error(err)
        else:
            products_list = []
            for element in soup.find_all('div', attrs={'data-cy': 'l-card'}):
                try:
                    name = element.find('h6').text
                    price = element.find('p', attrs={'data-testid': "ad-price"}).text.split('.')[0]
                    image_url = element.find('div', attrs={'type': "list"}).find('div').find('img').get("src")
                    products_list.append(
                        {
                            'name': name,
                            'description': name,
                            'price': price,
                            'category': category_name,
                            'image': image_url,
                        }
                    )
                except (AssertionError, KeyError) as err:
                    logger.error(err)
            return products_list



products_parser = Parser()

