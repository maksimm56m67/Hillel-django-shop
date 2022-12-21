
from django.urls import reverse
from django.core import mail
from items.models import Item, FavoriteProduct
from django.urls import reverse


def test_main_page(client, faker, product_factory):
    response = client.get(reverse('about'))
    assert response.status_code == 200
    

    data = {
        'email': faker.email(),
        'text': faker.sentence()
    }
    response = client.post(reverse('about'), data=data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('about') for i in response.redirect_chain)
    assert data['email'] in mail.outbox[0].body
    assert data['text'] in mail.outbox[0].body



def test_products_list(login_user, product_factory, faker):
    client, user = login_user
    response = client.get(reverse('main'))
    assert response.status_code == 200
    assert not response.context['object_list']

    product = product_factory()
    response = client.get(reverse('main'))
    assert response.status_code == 200
    assert len(response.context['object_list']) == 3

    response = client.get(reverse('product_detail', args=(faker.uuid4(),)))
    assert response.status_code == 404

    response = client.get(reverse('product_detail', args=(str(product.id),)))
    assert response.status_code == 200


def test_add_and_delete_favorites(client, faker, product_factory):
    
    url = reverse('favorites')
    
    data = {
        'product_uuid': faker.uuid4()
    }


    response = client.post(reverse('add_or_remove_favorite'), data=data, follow=True)
    assert response.status_code == 200
    assert product_factory in response.context_data['favorites'].items.iterator()
    