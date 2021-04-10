import random

def get_full_name(s: str):
    match = {"w": "Werewolf", "m": "Minion", "M": "Mason", "s": "Seer", "r":"Robber", "t": "TroubleMaker", "d": "Drunk", "v": "Villager", "i": "Insomniac", "T": "Tanner", "h": "Hunter", "D": "Doppelganger"}
    return match[s]

def get_role_by_pos(roles: str, pos: int):
    return get_full_name(roles[pos-1:pos])

def swap_card(r:str, op1:int, op2:int):
    if op1 == op2:
        return roles
    if op1 > op2:
        op1 = op1 + op2
        op2 = op1 - op2
        op1 = op1 - op2
    return r[0:op1-1] + r[op2-1:op2] + r[op1:op2-1] + r[op1-1:op1] + r[op2:]

def fetch_all_pos_by_role_name(roles: str, name: str):
    start = 0
    ret = list()
    start = roles.find(name, start, len(roles)-3)
    if start != -1:
        ret.append(start + 1)
    while start != -1:
        start = roles.find(name, start + 1, len(roles)-3)
        if start != -1:
            ret.append(start + 1)
    return ret

def fetch_all_werewolves(roles:str):
    return fetch_all_pos_by_role_name(roles, "w")

def fetch_all_masons(roles:str):
    return fetch_all_pos_by_role_name(roles, "M")

def valid_action_to_player(roles, op):
    return op > 0 and op < len(roles) - 3

def take_action(roles:str, pos: int, op1: int, op2: int)->tuple:
    ret = tuple()
    r = get_role_by_pos(roles, pos)
    if r == "Werewolf" or r == "Minion":
        ret = (roles, "All Werewolves are player " + " ".join(str(elem) for elem in fetch_all_werewolves(roles)))
    elif r == "Mason":
        ret = (roles, "All Masons are player " + " ".join(str(elem) for elem in fetch_all_masons(roles)))
    elif r == "Seer":
        if op2 == -1:
            if not valid_action_to_player(roles, op1):
                return (roles, "no action")
            ret = (roles, "Player " + str(op1) + " is " + get_role_by_pos(roles, op1))
        else:
            if op1 <= len(roles) - 3 or op2 <= len(roles) - 3 or op1 > len(roles) or op2 > len(roles):
                return (roles, "no action")
            ret = (roles, "Card " + str(op1+3-len(roles)) + " is " + get_role_by_pos(roles, op1) + ". Card " + str(op2+3-len(roles)) + " is " + get_role_by_pos(roles, op2))
    elif r == "Robber":
        if not valid_action_to_player(roles, op1) or op1 == pos:
            return (roles, "no action")
        swapped = swap_card(roles, pos, op1)
        ret = (swapped, "New role is " + get_role_by_pos(swapped, pos))
    elif r == "TroubleMaker":
        if op1 == -1 or op2 == -1 or not valid_action_to_player(roles, op1) or not valid_action_to_player(roles, op2) or op1 == op2:
            return (roles, "no action")
        ret = (swap_card(roles, op1, op2), "Player " + str(op1) + " and " + str(op2) + " are swapped")
    elif r == "Villager" or r == "Tanner" or r == "Hunter":
        ret = (roles, "no action")
    else:
        return "not support"
    return ret

