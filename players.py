# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = players_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


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


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Balance:
    id: Optional[str] = None
    mint: Optional[str] = None
    quantity: Optional[int] = None
    value_per_asset: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Balance':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        mint = from_union([from_str, from_none], obj.get("mint"))
        quantity = from_union([from_int, from_none], obj.get("quantity"))
        value_per_asset = from_union([from_float, from_none], obj.get("valuePerAsset"))
        return Balance(id, mint, quantity, value_per_asset)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["mint"] = from_union([from_str, from_none], self.mint)
        result["quantity"] = from_union([from_int, from_none], self.quantity)
        result["valuePerAsset"] = from_union([to_float, from_none], self.value_per_asset)
        return result


@dataclass
class Player:
    updated_at: Optional[datetime] = None
    avatar_id: Optional[str] = None
    badge_mint: Optional[str] = None
    id: Optional[str] = None
    public_key: Optional[str] = None
    balance: Optional[int] = None
    balances: Optional[List[Balance]] = None
    currency_symbol: Optional[str] = None
    faction: Optional[int] = None
    faction_rank: Optional[int] = None
    rank: Optional[int] = None
    registration_date: Optional[datetime] = None
    country: Optional[str] = None
    v: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Player':
        assert isinstance(obj, dict)
        updated_at = from_union([from_datetime, from_none], obj.get("updatedAt"))
        avatar_id = from_union([from_none, from_str], obj.get("avatarId"))
        badge_mint = from_union([from_none, from_str], obj.get("badgeMint"))
        id = from_union([from_str, from_none], obj.get("_id"))
        public_key = from_union([from_str, from_none], obj.get("publicKey"))
        balance = from_union([from_int, from_none], obj.get("balance"))
        balances = from_union([lambda x: from_list(Balance.from_dict, x), from_none], obj.get("balances"))
        currency_symbol = from_union([from_str, from_none], obj.get("currencySymbol"))
        faction = from_union([from_int, from_none], obj.get("faction"))
        faction_rank = from_union([from_int, from_none], obj.get("factionRank"))
        rank = from_union([from_int, from_none], obj.get("rank"))
        registration_date = from_union([from_datetime, from_none], obj.get("registrationDate"))
        country = from_union([from_str, from_none], obj.get("country"))
        v = from_union([from_int, from_none], obj.get("__v"))
        return Player(updated_at, avatar_id, badge_mint, id, public_key, balance, balances, currency_symbol, faction, faction_rank, rank, registration_date, country, v)

    def to_dict(self) -> dict:
        result: dict = {}
        result["updatedAt"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        result["avatarId"] = from_union([from_none, from_str], self.avatar_id)
        result["badgeMint"] = from_union([from_none, from_str], self.badge_mint)
        result["_id"] = from_union([from_str, from_none], self.id)
        result["publicKey"] = from_union([from_str, from_none], self.public_key)
        result["balance"] = from_union([from_int, from_none], self.balance)
        result["balances"] = from_union([lambda x: from_list(lambda x: to_class(Balance, x), x), from_none], self.balances)
        result["currencySymbol"] = from_union([from_str, from_none], self.currency_symbol)
        result["faction"] = from_union([from_int, from_none], self.faction)
        result["factionRank"] = from_union([from_int, from_none], self.faction_rank)
        result["rank"] = from_union([from_int, from_none], self.rank)
        result["registrationDate"] = from_union([lambda x: x.isoformat(), from_none], self.registration_date)
        result["country"] = from_union([from_str, from_none], self.country)
        result["__v"] = from_union([from_int, from_none], self.v)
        return result


def players_from_dict(s: Any) -> List[Player]:
    return from_list(Player.from_dict, s)


def players_to_dict(x: List[Player]) -> Any:
    return from_list(lambda x: to_class(Player, x), x)
