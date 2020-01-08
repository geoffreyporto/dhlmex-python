import os
from typing import Dict
from urllib import parse

import pytest
from vcr import request

from dhlmex import Client
from dhlmex.resources.urls import dhl_urls

DHLMEX_USERNAME = os.environ["DHLMEX_USERNAME"]
DHLMEX_PASSWORD = os.environ["DHLMEX_PASSWORD"]


def remove_creds(req: request.Request) -> request.Request:
    if req.path.endswith(dhl_urls['login']) and req.method == 'POST':
        username_key = 'j_id6:j_id20'
        password_key = 'j_id6:j_id22'
        body = parse.parse_qs(req.body.decode('utf-8'))
        body[username_key] = ['USERNAME']
        body[password_key] = ['PASSWORD']
        req.body = parse.urlencode(body)
    return req


@pytest.fixture(scope='module')
def vcr_config() -> dict:
    config = dict(before_record_request=remove_creds)
    return config


@pytest.fixture
def site_urls() -> Dict:
    return dhl_urls


@pytest.fixture
def client():
    client = Client(DHLMEX_USERNAME, DHLMEX_PASSWORD)
    yield client
    client._logout()


@pytest.fixture
def origin_address() -> Dict:
    return dict(
        company='CUENCA LABS',
        contact='DANIEL ESPINABARRO LOPEZ',
        mail='del@cuenca.com',
        phone='5544364200',
        address1='VARSOVIA 36',
        postal_code='06600',
        neighborhood='JUAREZ',
        city='CUAUHTEMOC',
        state='CMX',
    )


@pytest.fixture
def destiny_address() -> Dict:
    return dict(
        company='IVANNA DÍAZ ESTRADA',
        contact='IVANNA DÍAZ ESTRADA',
        mail='ivanna.diaz.estrada@gmail.com',
        phone='5544364200',
        address1='CALLE 39 231',
        postal_code='97320',
        neighborhood='VICENTE GUERRERO',
        city='PROGRESO',
        state='YUC',
    )


@pytest.fixture
def details() -> Dict:
    return dict(
        description='CASA COLOR VERDE', content='Tarjetas de presentacion',
    )
