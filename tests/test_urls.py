import pytest

from django.urls import reverse, resolve


@pytest.mark.urls_path
def test_urls_path_all_rooms():
    assert "/all_rooms/" == reverse("all_rooms")


@pytest.mark.urls_path
def test_urls_path_room_new():
    assert "/room/new/" == reverse("room_new")


@pytest.mark.urls_path
def test_urls_path_room_image_upload():
    assert "/room/image/upload/1" == reverse("room_image_upload", kwargs={"pk": 1})


@pytest.mark.urls_path
def test_urls_path_room_image_delete():
    assert "/room/image/remove/" == reverse(
        "room_image_delete",
    )


@pytest.mark.urls_path
def test_urls_path_room_delete():
    assert "/room/delete/1" == reverse("room_delete", kwargs={"pk": 1})


@pytest.mark.urls_path
def test_urls_path_room_detail():
    assert "/room/1" == reverse("room_detail", kwargs={"pk": 1})


@pytest.mark.urls_path
def test_urls_path_reservation_delete():
    assert "/room/reservation/delete/1" == reverse(
        "reservation_delete", kwargs={"pk": 1}
    )


@pytest.mark.urls_path
def test_urls_path_room_edit():
    assert "/room/modify/1" == reverse("room_edit", kwargs={"pk": 1})


@pytest.mark.urls_path
def test_urls_path_search():
    assert "/search/" == reverse("search")


@pytest.mark.urls_path
def test_urls_path_reservation():
    assert "/reservation/1" == reverse("reservation", kwargs={"pk": 1})
