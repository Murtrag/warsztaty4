import os
import datetime

from mixer.backend.django import mixer


def test_is_booked():
    room_booked = mixer.blend("page.Reservation", date=datetime.datetime.today()).rooms
    room_unbooked = mixer.blend("page.Room")
    assert room_booked.is_booked is True
    assert room_unbooked.is_booked is False


def test_room_str():
    name = "test"
    room = mixer.blend("page.Room", name=name)
    assert str(room) == name


def test_image_str():
    image = mixer.blend("page.Image")
    _, file = os.path.split(image.image.path)
    assert str(image) == os.path.splitext(file)[0]


# class TestClass:
# 	def setup_method(self):
# 		print("--------setup")
# 	def teardown_method(self):
# 		print('-------teardown')
# 	def test_one(self, dummy_room):
# 		assert 1==1
