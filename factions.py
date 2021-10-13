# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = factions_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Value:
    currency_symbol: Optional[str] = None
    total: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Value':
        assert isinstance(obj, dict)
        currency_symbol = from_union([from_str, from_none], obj.get("currencySymbol"))
        total = from_union([from_int, from_none], obj.get("total"))
        return Value(currency_symbol, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currencySymbol"] = from_union([from_str, from_none], self.currency_symbol)
        result["total"] = from_union([from_int, from_none], self.total)
        return result


@dataclass
class TopPlayer:
    public_key: Optional[str] = None
    value: Optional[Value] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TopPlayer':
        assert isinstance(obj, dict)
        public_key = from_union([from_str, from_none], obj.get("publicKey"))
        value = from_union([Value.from_dict, from_none], obj.get("value"))
        return TopPlayer(public_key, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["publicKey"] = from_union([from_str, from_none], self.public_key)
        result["value"] = from_union([lambda x: to_class(Value, x), from_none], self.value)
        return result


@dataclass
class Faction:
    faction: Optional[int] = None
    total_players: Optional[int] = None
    value: Optional[Value] = None
    top_player: Optional[TopPlayer] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Faction':
        assert isinstance(obj, dict)
        faction = from_union([from_int, from_none], obj.get("faction"))
        total_players = from_union([from_int, from_none], obj.get("totalPlayers"))
        value = from_union([Value.from_dict, from_none], obj.get("value"))
        top_player = from_union([TopPlayer.from_dict, from_none], obj.get("topPlayer"))
        return Faction(faction, total_players, value, top_player)

    def to_dict(self) -> dict:
        result: dict = {}
        result["faction"] = from_union([from_int, from_none], self.faction)
        result["totalPlayers"] = from_union([from_int, from_none], self.total_players)
        result["value"] = from_union([lambda x: to_class(Value, x), from_none], self.value)
        result["topPlayer"] = from_union([lambda x: to_class(TopPlayer, x), from_none], self.top_player)
        return result


def factions_from_dict(s: Any) -> List[Faction]:
    return from_list(Faction.from_dict, s)


def factions_to_dict(x: List[Faction]) -> Any:
    return from_list(lambda x: to_class(Faction, x), x)
