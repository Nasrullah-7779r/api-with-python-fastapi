import pdb

import pytest
from fastapi import status
from app2 import schemas


# def test_get_all_notes(test_notes):
#     res = test_notes.authorized_client.get("/all_notes")
#     print(res.json())
#     assert res.status_code == status.HTTP_200_OK
@pytest.mark.skip
def test_get_all_notes(authorized_client, test_notes):
    res = authorized_client.get("/all_notes")

    # print(res.json())
    def validate(note):
        return schemas.NoteOut(**note)

    note_map = map(validate, res.json())
    print(list(note_map))
    assert len(res.json()) == len(test_notes)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.skip
def test_unauthorized_user_get_all_notes(client, test_notes):
    res = client.get("/all_notes")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.skip
def test_get_one_note_not_exist(authorized_client, test_notes):
    res = authorized_client.get(f"/one_note/800054654")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.skip
def test_get_one_note(authorized_client, test_notes):
    # pdb.set_trace()
    res = authorized_client.get(f"/one_note/{test_notes[0].id}")

    print(f"res is {res.json()}")
    note = schemas.NoteOut(**res.json())
    print(res.json())
    assert note.id == test_notes[0].id


# @pytest.mark.skip
@pytest.mark.parametrize("title, description", [
    ("Love", "Love is beautiful emotion"),
    ("Dream", "Dreams are product of your mind"),
    ("Fear", "Fear is the strong emotion, which definitely need to be controlled")
])
def test_create_note(authorized_client, test_user, title, description):
    res = authorized_client.post("/create_note",
                                 json={"title": title, "description": description})
    # pdb.set_trace()
    created_note = {"title": res.json()["New Note"]["title"], "description": res.json()["New Note"]["description"]}

    print(res.json())
    # created_post = schemas.NoteCreate(**res.json())

    assert res.status_code == 201
    assert created_note["title"] == title
    assert created_note["description"] == description
