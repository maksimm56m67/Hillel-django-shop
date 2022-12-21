import decimal
import io
import uuid

from django.core.mail import mail_managers
from currencies.models import Config
from shop.celery import app


from django.core.files.images import ImageFile

from items.client.client import products_parser
from items.models import Category, Item
from shop.api_clients import BaseClient
from shop.celery import app

@app.task
def send_contact_form(email, text):
    mail_managers('Contact form', f'From: {email}\n{text}' [Config.load().contact_form_email])




@app.task
def save_parsed_products(products_list: list):
    if not products_list:
        return
    
    request_client = BaseClient()
    
    for product_dict in products_list:
 
        category, _ = Category.objects.get_or_create(
            name=product_dict['category'],
        )      

        response = request_client.get_request(
            url=product_dict['image'],
            method='get'
        )
        
        image = ImageFile(io.BytesIO(response), name='image.jpg')
        price = decimal.Decimal(''.join(i for i in product_dict['price'] if i.isdigit()))

 

                
        product, created = Item.objects.get_or_create(
            name=product_dict['name'],
            category=category,
            defaults={
                'image': image,
                'description': product_dict['description'],
                'price': price
            }
        )
        if not created:
            product.price = price
            product.image = image
            product.save(update_fields=('price', 'image'))


@app.task
def parse_products():
    save_parsed_products(products_parser.parse())