import operator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from main import app
import gameengine as ge
import models

client = TestClient(app)

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
    assert ge.has_this_role_in_game(roles, "T") == False
    assert ge.has_this_role_in_game(roles, "h") == False
    assert ge.has_this_role_in_game(roles, "D") == False
    assert ge.has_this_role_in_game(roles, "d") == False
    assert ge.has_this_role_in_game(roles, "t")
    assert ge.has_this_role_in_game(roles, "w")
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
    roles = 'divMMsrtwwm'
    assert ge.take_action(roles, 1, 2, -1) == ('divMMsrtwwm', "no action")
    assert ge.take_action(roles, 1, -1, -1) == ('divMMsrtwwm', "no action")
    assert ge.take_action(roles, 1, 11, -1) == ('mivMMsrtwwd', "Swapped with card 3")
    assert ge.take_action(roles, 1, 9, -1) == ('wivMMsrtdwm', "Swapped with card 1")
    assert ge.take_action(roles, 2, -1, -1) == ('divMMsrtwwm', "Now you are Insomniac")

def test_game_engine_all_actions():
    # test case 1
    player1 = models.Player(rmid=1, pos=1, name="p1", op1=-1, op2=-1, awaken=1, voted=-1)
    player2 = models.Player(rmid=1, pos=2, name="p2", op1=-1, op2=-1, awaken=1, voted=-1)
    player3 = models.Player(rmid=1, pos=3, name="p3", op1=-1, op2=-1, awaken=1, voted=-1)
    player4 = models.Player(rmid=1, pos=4, name="p4", op1=-1, op2=-1, awaken=1, voted=-1)
    player5 = models.Player(rmid=1, pos=5, name="p5", op1=-1, op2=-1, awaken=1, voted=-1)
    player6 = models.Player(rmid=1, pos=6, name="p6", op1=3, op2=-1, awaken=1, voted=-1)
    player7 = models.Player(rmid=1, pos=7, name="p7", op1=3, op2=-1, awaken=1, voted=-1)
    player8 = models.Player(rmid=1, pos=8, name="p8", op1=5, op2=7, awaken=1, voted=-1)
    player_list = [player1, player2, player3, player4, player5, player6, player7, player8]
    roles="wwmMMsrtdiv"
    (roles_in_game, ret_map) = ge.take_all_actions(player_list, roles)
    assert roles_in_game == 'wwrMmsMtdiv'
    assert ret_map[6] == "Player 3 is Minion"
    assert ret_map[7] == "New role is Minion"

    # test case 2
    player1 = models.Player(rmid=1, pos=1, name="p1", op1=-1, op2=-1, awaken=1, voted=-1)
    player2 = models.Player(rmid=1, pos=2, name="p2", op1=10, op2=-1, awaken=1, voted=-1)
    player3 = models.Player(rmid=1, pos=3, name="p3", op1=-1, op2=-1, awaken=1, voted=-1)
    player4 = models.Player(rmid=1, pos=4, name="p4", op1=-1, op2=-1, awaken=1, voted=-1)
    player5 = models.Player(rmid=1, pos=5, name="p5", op1=-1, op2=-1, awaken=1, voted=-1)
    player6 = models.Player(rmid=1, pos=6, name="p6", op1=2, op2=-1, awaken=1, voted=-1)
    player7 = models.Player(rmid=1, pos=7, name="p7", op1=2, op2=-1, awaken=1, voted=-1)
    player8 = models.Player(rmid=1, pos=8, name="p8", op1=1, op2=2, awaken=1, voted=-1)
    player_list = [player1, player2, player3, player4, player5, player6, player7, player8]
    roles="idmMMsrtwwv"
    (roles_in_game, ret_map) = ge.take_all_actions(player_list, roles)
    assert roles_in_game == 'rwmMMsdtwiv'
    assert ret_map[1] == "Now you are Robber"
    assert ret_map[7] == "New role is Drunk"
    assert ret_map[6] == "Player 2 is Drunk"
    assert ret_map[3] == "No Werewolf"
