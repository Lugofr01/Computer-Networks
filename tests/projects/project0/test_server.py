import pytest
from src.projects.project0.server import format, parse


@pytest.mark.parametrize(
    "message, data",
    [
        ("Toph", b"Hello, Toph"),
        ("The Child", b"Hello, The Child"),
        (
            "フンベルト・フォン・ジッキンゲン",
            b"Hello, \xe3\x83\x95\xe3\x83\xb3\xe3\x83\x99\xe3\x83\xab\xe3\x83\x88\xe3\x83\xbb\xe3\x83\x95\xe3\x82\xa9\xe3\x83\xb3\xe3\x83\xbb\xe3\x82\xb8\xe3\x83\x83\xe3\x82\xad\xe3\x83\xb3\xe3\x82\xb2\xe3\x83\xb3",
        ),
        (
            "Чорна вдова",
            b"Hello, \xd0\xa7\xd0\xbe\xd1\x80\xd0\xbd\xd0\xb0 \xd0\xb2\xd0\xb4\xd0\xbe\xd0\xb2\xd0\xb0",
        ),
    ],
)
def test_server_format(message, data):
    assert format(message) == data


@pytest.mark.parametrize(
    "data, message",
    [
        (b"Hello, my name is Toph", "Toph"),
        (b"Hello, my name is The Child", "The Child"),
        (
            b"Hello, my name is \xe3\x83\x95\xe3\x83\xb3\xe3\x83\x99\xe3\x83\xab\xe3\x83\x88\xe3\x83\xbb\xe3\x83\x95\xe3\x82\xa9\xe3\x83\xb3\xe3\x83\xbb\xe3\x82\xb8\xe3\x83\x83\xe3\x82\xad\xe3\x83\xb3\xe3\x82\xb2\xe3\x83\xb3",
            "フンベルト・フォン・ジッキンゲン",
        ),
        (
            b"Hello, my name is \xd0\xa7\xd0\xbe\xd1\x80\xd0\xbd\xd0\xb0 \xd0\xb2\xd0\xb4\xd0\xbe\xd0\xb2\xd0\xb0",
            "Чорна вдова",
        ),
    ],
)
def test_server_parse(data, message):
    assert parse(data) == message


if __name__ == "__main__":
    pytest.main()
