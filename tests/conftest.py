import pytest
import datetime

from page.models import Room, Reservation, Image
from mixer.backend.django import mixer


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture
def dummy_reservation(django_db_blocker):
    return mixer.cycle(10).blend('page.Reservation')

@pytest.fixture
def dummy_room(dummy_reservation):
    ret = list()
    for reservation in dummy_reservation:
        ret.append(reservation.rooms)
    return ret

@pytest.fixture
def dummy_immage():
    return mixer.blend('page.Image')
