import operator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from main import app
import gameengine as ge

client = TestClient(app)

# def test_index():
    # response = client.get("/index")
    # assert response.status_code == 200
    # assert response.json() == {"msg": "欢迎来到SayHello!"}


# @pytest.mark.parametrize("skip, limit", [[1, 2], [1, 10], [-1, 5]])
# def test_get_message(skip, limit):
    # response = client.get("/message", params={"skip": skip, "limit": limit})
    # assert response.status_code == 200
    # sql = "select * from message order by create_at desc limit :skip,:limit"
    # data = session.execute(text(sql), {"skip": skip, "limit": limit}).fetchall()
    # assert response.json()['data'][0]["id"] == data[0]["id"]


# @pytest.mark.parametrize("data", [{"name": "七七", "body": "回踩!"}])
# def test_add_message(data):
    # response = client.post("/message", json=data)
    # assert response.status_code == 200
    # sql = "select * from message where name = :name"
    # result = session.execute(text(sql), {"name": data["name"]}).fetchall()
    # assert result is not None

# def test_index():
    # response = client.get("/index")
    # assert response.status_code == 200


def test_create_game():
    client.post("/onenightwolf/playground/delete/room/1")
    resonse = client.post("/onenightwolf/playground/create/room/1/ri/abc")
    assert resonse.status_code == 200

def test_get_game():
    response = client.get("/onenightwolf/playground/search/room/1")
    assert response.status_code == 200
    assert response.json() == {
        "rmid" : 1,
        "rolesinit" : "abc",
        "rolesingame": "abc"
    }

def test_create_player():
    response = client.post("/onenightwolf/prepare/create/room/1/pos/2/name/test")
    assert response.status_code == 200
    assert response.json()["rmid"] == 1
    assert response.json()["pos"] == 2
    assert response.json()["name"] == "test"

def test_get_player():
    response = client.get("/onenightwolf/prepare/search/room/1/pos/2/name/test")
    assert response.status_code == 200
    response = client.get("/onenightwolf/prepare/search/room/1/pos/2/name/test2")
    assert response.status_code == 404

def test_game_engine():
    roles = 'wwmMMsrtdiv'
    assert ge.fetch_all_masons(roles) == [4,5]
    assert ge.fetch_all_werewolves(roles) == [1,2]
    roles1 = 'wimMMsrtdwv'
    assert ge.fetch_all_werewolves(roles1) == [1]
    assert ge.fetch_all_pos_by_role_name(roles, 'T') == []
    assert ge.swap_card(roles,2,3) == 'wmwMMsrtdiv'
    assert ge.swap_card(roles,11,1) == 'vwmMMsrtdiw'
    assert ge.swap_card(roles,1,9) == 'dwmMMsrtwiv'
    assert ge.take_action(roles, 1, -1, -1) == ('wwmMMsrtdiv', "All Werewolves are player 1 2")
    assert ge.take_action(roles, 2, -1, -1) == ('wwmMMsrtdiv', "All Werewolves are player 1 2")
    assert ge.take_action(roles, 3, -1, -1) == ('wwmMMsrtdiv', "All Werewolves are player 1 2")
    assert ge.take_action(roles, 4, -1, -1) == ('wwmMMsrtdiv', "All Masons are player 4 5")
    assert ge.take_action(roles, 5, -1, -1) == ('wwmMMsrtdiv', "All Masons are player 4 5")
    assert ge.take_action(roles, 6, 2, -1) == ('wwmMMsrtdiv', "Player 2 is Werewolf")
    assert ge.take_action(roles, 6, 9, -1) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 6, 9, 11) == ('wwmMMsrtdiv', "Card 1 is Drunk. Card 3 is Villager")
    assert ge.take_action(roles, 6, 4, 11) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 6, 9, 13) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 6, 13, 11) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 6, -1, -1) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 7, -1, -1) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 7, 1, -1) == ('rwmMMswtdiv', "New role is Werewolf")
    assert ge.take_action(roles, 7, 5, -1) == ('wwmMrsMtdiv', "New role is Mason")
    assert ge.take_action(roles, 7, 7, -1) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 7, 10, -1) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 8, 10, -1) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 8, -1, -1) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 8, 5, 5) == ('wwmMMsrtdiv', "no action")
    assert ge.take_action(roles, 8, 2, 5) == ('wMmMwsrtdiv', "Player 2 and 5 are swapped")
