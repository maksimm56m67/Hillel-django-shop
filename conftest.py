import pytest

import factory
import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from faker import Faker
from pytest_factoryboy import register

from items.models import Item, Category
from shop.constants import DECIMAL_PLACES
from django.contrib.auth import get_user_model
from faker import Faker
from items.models import Category, Item
from django.urls import reverse
from django.test.client import Client

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    from pprint import pp
    __builtins__['pp'] = pp
    # code before tests run
    yield
    del __builtins__['pp']
    # code after tests run
fake = Faker()
User = get_user_model()

def faker():
    yield fake

@pytest.fixture(scope='function')
def user(db):
    user, _ = User.objects.get_or_create(
        email='user@user.com',
        first_name='John Smith',
        phone='123456789',
        is_phone_valid=True
    )
    user.set_password('123456789')
    user.save()
    yield user


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda x: fake.email())
    first_name = factory.Sequence(lambda x: fake.name())
    last_name = factory.Sequence(lambda x: fake.name())


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda x: fake.name())
    description = factory.Sequence(lambda x: fake.name())
    image = factory.django.ImageField()


@register
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item
        django_get_or_create = ('name', 'category')
        
    name = factory.Sequence(lambda x: fake.name())
    image = factory.django.ImageField()
    price = factory.Sequence(lambda x: fake.pydecimal(
        min_value=1,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES,
    ))
    category = factory.SubFactory(CategoryFactory)
    
    @factory.post_generation
    def post_create(self, created, *args, **kwargs):
        if created and not kwargs.get('deny_post'):
            for _ in range(1, 3):
                self.items.add(
                    ProductFactory(post_create__deny_post=True)
                )


@pytest.fixture(scope='function')
def login_user(db):
    phone = '123456789'
    password = '123456789'
    user = UserFactory(phone=phone, is_phone_valid=True)
    user.set_password(password)
    user.save()
    client = Client()
    response = client.post(reverse('login'), data={'phone': phone,
                                                   'password': password})
    assert response.status_code == 302
    yield client, user


   