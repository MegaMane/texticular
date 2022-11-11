from texticular.game_object import GameObject
import pytest
from pytest import raises
from itertools import count

"""
Test cases
x Can create game object
x can Look at a game object by calling command "look" and returns passed in main description
x Can Examine a game object by calling command "examine" and returns passed in examine description
x Can set current_description
x can set examine description
x Can lookup an object by key value and return it using class method lookup_by_key
x Can move a game object to another location (game object)
x Can remove a game object from a location
x Can add a flags to a game object
x Can remove a flag rom a game object
can print a game object __repr__ method
Can call custom Action method
can serialize a game object to json


"""


@pytest.fixture(scope="module")
def game_object():
    game_object = GameObject(key_value="office_lock",
                             name="lock",
                             descriptions={
                                 "Main": "A little grey padlock",
                                 "Examine": "It's full of tiny little ridges, dings, and dents.",
                                 "Description-GummedUp": "The lock has a piece of gum jammed in it, no key will open it now.",
                                 "Examine-Discover": "Etched at the bottom of the lock is a faint 4 digit code. It reads 8745."
                             }
                             )
    return game_object





def test_canLookAtObject(game_object):
    assert game_object.describe() == game_object.current_description


def test_canExamineObject(game_object):
    assert game_object.examine() == game_object.examine_description


def test_canSetDescription(game_object):
    previous_descript = game_object.current_description
    game_object.current_description = "Description-GummedUp"
    assert game_object.current_description != previous_descript


def test_canFetchGameObjectByKey():
    game_object = GameObject.lookup_by_key("office_lock")
    assert game_object


def test_raisesValueError_OnDuplicateObjectCreation(game_object):
    with raises(ValueError):
        duplicate_object = GameObject(key_value="office_lock",
                                      name="duplicate lock",
                                      descriptions={"Main": "A duplicate lock"}
                                      )


def test_canMoveGameObject(game_object):
    new_location = GameObject(
                              key_value="office_desk",
                              name="desk",
                              descriptions={"Main": "A basic ass desk."}
                              )
    game_object.move("office_desk")


def test_raisesValueError_WhenMovingObjectToInvalidLocation(game_object):
    with raises(ValueError):
        game_object.move("bogus location")

def test_canRemoveGameObjectFromMap(game_object):
    game_object.remove()
    assert game_object.location_key is None

def test_canAddFlagsToGameObject(game_object):
    game_object.add_flag("TAKEBIT")
    game_object.add_flag("LOCKEDBIT")
    assert len(game_object.flags) == 2

def test_raisesValueError_WhenFlagIsNotValidEnumMember(game_object):
    with raises(ValueError):
        game_object.add_flag("FAKEBIT")

def test_canInstantiateGameObjectWithFlags():
    set_piece = GameObject(
        key_value="office_painting",
        name="painting",
        descriptions={"Main": "A tacky piece of art."},
        flags=["SETPIECEBIT","TAKEBIT"]
    )

def test_raisesValueError_WhenObjectInstantiatedWithInvalidFlag():
    with raises(ValueError):
        set_piece = GameObject(
            key_value="office_painting",
            name="painting",
            descriptions={"Main": "A tacky piece of art."},
            flags=["SETPIECEBIT","FAKEBIT"]
        )

def test_canRemoveFlag(game_object):
    game_object.flags = set()
    game_object.add_flag("SETPIECEBIT")
    game_object.remove_flag("SETPIECEBIT")
    assert len(game_object.flags) == 0

def test_ReturnFalseWhenRemovingFlagThatDoesNotExist(game_object):
    assert game_object.remove_flag("NonExistant") == False




@pytest.mark.skip
def test_canCallcustomActionMethod(game_object):
    def my_custom_action(controller, target: GameObject):
        response = f"Hey {target.name} get back to work!"
        return True

    game_object.action = my_custom_action
    result = game_object.action(controller="controller", target=game_object)
    assert result == "Hey lock get back to work!"


def test_canPrintGameObject(game_object):
    print(game_object)
    assert True
