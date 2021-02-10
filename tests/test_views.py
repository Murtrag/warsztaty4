import json
import pytest
import datetime

from django.urls import reverse
from django.test import TestCase
from mixer.backend.django import mixer
from django.contrib.messages import get_messages


@pytest.mark.views
def test_view_room_list(client):
    response = client.get(reverse("all_rooms"))
    assert response.status_code == 200
    assert "Wynajem salek konferencyjnych" in str(response.content)


class TestAddRoom:
    def setup_method(self):
        self.url = reverse("room_new")
        self.data = {
            "name": "test",
            "capacity": 2,
            "projector": True,
            "tv": False,
            "air_conditioning": True,
        }

    def test_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        assert "Wynajem salek konferencyjnych" in str(response.content)

    def test_post(self, client):
        response = client.post(self.url, data=self.data)
        assert response.status_code == 302


# @pytest.mark.views
# def test_view_upload_image(client):
# 	response = client.post(
# 		reverse(
# 				"room_image_upload",
# 				kwargs={'pk': 1}
# 			)
# 	)
# 	assert response.status_code == 200
# 	assert 'Wynajem salek konferencyjnych' in str(response.content)


@pytest.mark.views
def test_view_delete_file(client, dummy_immage):
    data = {"file_name": str(dummy_immage)}
    response = client.post(
        reverse(
            "room_image_delete",
        ),
        json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200


@pytest.mark.views
def test_view_detail_room(client, dummy_room):
    response = client.get(reverse("room_detail", kwargs={"pk": dummy_room[0].pk}))
    assert response.status_code == 200
    assert "Wynajem salek konferencyjnych" in str(response.content)


@pytest.mark.views
def test_view_delete_room(client, dummy_room):
    response = client.post(
        reverse(
            "room_delete",
            kwargs={"pk": dummy_room[0].pk},  # dummy_room is called again so pk inc
        )
    )
    assert response.status_code == 302
    "Czy na pewno chcesz usunąć salkę" in response.content.decode("utf-8")


class TestDeleteReservation:
    def _url(self, objects):
        return reverse("reservation_delete", kwargs={"pk": objects[0].pk})

    def test_get(self, client, dummy_reservation):
        response = client.get(self._url(dummy_reservation))
        assert response.status_code == 200

    def test_post(self, client, dummy_reservation):
        response = client.post(self._url(dummy_reservation))
        assert response.status_code == 302


class TestEditRoom:
    def setup_method(self):
        self.data = {
            "name": "test",
            "capacity": 2,
            "projector": True,
            "tv": True,
            "air_conditioning": True,
        }

    def _url(self, objects):
        return reverse(
            "room_edit",
            kwargs={"pk": objects[0].pk},
        )

    def test_get(self, client, dummy_room):
        response = client.get(self._url(dummy_room))
        assert response.status_code == 200

    def test_post(self, client, dummy_room):
        response = client.post(self._url(dummy_room), data=self.data)
        assert response.status_code == 302


class TestViewSearch:
    def setup_method(self):
        self.url = reverse("search")
        self.data = {
            "least_capacity": 2,
            "projector": True,
            "tv": True,
            "air_conditioning": True,
        }

    def test_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200

    def test_get_param(self, client):
        response = client.get(
            self.url,
            data={**self.data, "date": datetime.datetime.today().strftime("%Y-%m-%d")},
        )
        assert response.status_code == 200

    def test_get_param_no_data(self, client):
        response = client.get(self.url, data=self.data)
        assert response.status_code == 200


@pytest.mark.parametrize(
    "data, result_status, message",
    [
        ("", 302, "nie podano daty!"),  # no string
        (datetime.datetime.today().strftime("%Y-%m-%d"), 302, None),  # today
        (
            (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d"),
            302,
            "przeszłości",
        ),  # yesterday
        (
            (datetime.datetime.now() + datetime.timedelta(1)).strftime("%Y-%m-%d"),
            302,
            "zarezerwowana",
        ),  # tomorrow booked
    ],
)
@pytest.mark.views
def test_view_reseration(client, dummy_room, data, result_status, message):
    mixer.blend(
        "page.Reservation",
        date=(datetime.datetime.now() + datetime.timedelta(1)).strftime("%Y-%m-%d"),
        rooms=dummy_room[0],
    )

    data = {"date": data, "client": "Michael Jordan"}
    response = client.post(
        reverse("reservation", kwargs={"pk": dummy_room[0].pk}), data=data
    )
    try:
        response_message = list(get_messages(response.wsgi_request))[0].message
    except IndexError:
        response_message = [None]

    assert response.status_code == result_status
    assert message in response_message
