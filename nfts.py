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
#     result = nfts_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
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


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Airdrop:
    id: Optional[str] = None
    supply: Optional[int] = None
    airdrop_id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Airdrop':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        supply = from_union([from_int, from_none], obj.get("supply"))
        airdrop_id = from_union([from_int, from_none], obj.get("id"))
        return Airdrop(id, supply, airdrop_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["supply"] = from_union([from_int, from_none], self.supply)
        result["id"] = from_union([from_int, from_none], self.airdrop_id)
        return result


@dataclass
class Attributes:
    item_type: Optional[str] = None
    rarity: Optional[str] = None
    tier: Optional[int] = None
    attributes_class: Optional[str] = None
    score: Optional[int] = None
    musician: Optional[str] = None
    spec: Optional[str] = None
    category: Optional[str] = None
    crew_slots: Optional[int] = None
    component_slots: Optional[int] = None
    module_slots: Optional[int] = None
    unit_length: Optional[float] = None
    unit_width: Optional[float] = None
    unit_height: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Attributes':
        assert isinstance(obj, dict)
        item_type = from_union([from_str, from_none], obj.get("itemType"))
        rarity = from_union([from_str, from_none], obj.get("rarity"))
        tier = from_union([from_int, from_none], obj.get("tier"))
        attributes_class = from_union([from_str, from_none], obj.get("class"))
        score = from_union([from_int, from_none], obj.get("score"))
        musician = from_union([from_str, from_none], obj.get("musician"))
        spec = from_union([from_str, from_none], obj.get("spec"))
        category = from_union([from_str, from_none], obj.get("category"))
        crew_slots = from_union([from_int, from_none], obj.get("crewSlots"))
        component_slots = from_union([from_int, from_none], obj.get("componentSlots"))
        module_slots = from_union([from_int, from_none], obj.get("moduleSlots"))
        unit_length = from_union([from_float, from_none], obj.get("unitLength"))
        unit_width = from_union([from_float, from_none], obj.get("unitWidth"))
        unit_height = from_union([from_float, from_none], obj.get("unitHeight"))
        return Attributes(item_type, rarity, tier, attributes_class, score, musician, spec, category, crew_slots, component_slots, module_slots, unit_length, unit_width, unit_height)

    def to_dict(self) -> dict:
        result: dict = {}
        result["itemType"] = from_union([from_str, from_none], self.item_type)
        result["rarity"] = from_union([from_str, from_none], self.rarity)
        result["tier"] = from_union([from_int, from_none], self.tier)
        result["class"] = from_union([from_str, from_none], self.attributes_class)
        result["score"] = from_union([from_int, from_none], self.score)
        result["musician"] = from_union([from_str, from_none], self.musician)
        result["spec"] = from_union([from_str, from_none], self.spec)
        result["category"] = from_union([from_str, from_none], self.category)
        result["crewSlots"] = from_union([from_int, from_none], self.crew_slots)
        result["componentSlots"] = from_union([from_int, from_none], self.component_slots)
        result["moduleSlots"] = from_union([from_int, from_none], self.module_slots)
        result["unitLength"] = from_union([to_float, from_none], self.unit_length)
        result["unitWidth"] = from_union([to_float, from_none], self.unit_width)
        result["unitHeight"] = from_union([to_float, from_none], self.unit_height)
        return result


@dataclass
class Market:
    id: Optional[str] = None
    market_id: Optional[str] = None
    quote_pair: Optional[str] = None
    serum_program_id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Market':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        market_id = from_union([from_str, from_none], obj.get("id"))
        quote_pair = from_union([from_str, from_none], obj.get("quotePair"))
        serum_program_id = from_union([from_str, from_none], obj.get("serumProgramId"))
        return Market(id, market_id, quote_pair, serum_program_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["id"] = from_union([from_str, from_none], self.market_id)
        result["quotePair"] = from_union([from_str, from_none], self.quote_pair)
        result["serumProgramId"] = from_union([from_str, from_none], self.serum_program_id)
        return result


@dataclass
class Media:
    qr_instagram: Optional[str] = None
    qr_facebook: Optional[str] = None
    audio: Optional[str] = None
    sketchfab: Optional[str] = None
    thumbnail_url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Media':
        assert isinstance(obj, dict)
        qr_instagram = from_union([from_str, from_none], obj.get("qrInstagram"))
        qr_facebook = from_union([from_str, from_none], obj.get("qrFacebook"))
        audio = from_union([from_str, from_none], obj.get("audio"))
        sketchfab = from_union([from_str, from_none], obj.get("sketchfab"))
        thumbnail_url = from_union([from_str, from_none], obj.get("thumbnailUrl"))
        return Media(qr_instagram, qr_facebook, audio, sketchfab, thumbnail_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["qrInstagram"] = from_union([from_str, from_none], self.qr_instagram)
        result["qrFacebook"] = from_union([from_str, from_none], self.qr_facebook)
        result["audio"] = from_union([from_str, from_none], self.audio)
        result["sketchfab"] = from_union([from_str, from_none], self.sketchfab)
        result["thumbnailUrl"] = from_union([from_str, from_none], self.thumbnail_url)
        return result


@dataclass
class PrimarySale:
    order_id: None
    id: Optional[str] = None
    list_timestamp: Optional[int] = None
    supply: Optional[int] = None
    price: Optional[int] = None
    is_minted: Optional[bool] = None
    is_listed: Optional[bool] = None
    mint_timestamp: Optional[int] = None
    expire_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PrimarySale':
        assert isinstance(obj, dict)
        order_id = from_none(obj.get("orderId"))
        id = from_union([from_str, from_none], obj.get("_id"))
        list_timestamp = from_union([from_int, from_none], obj.get("listTimestamp"))
        supply = from_union([from_int, from_none], obj.get("supply"))
        price = from_union([from_int, from_none], obj.get("price"))
        is_minted = from_union([from_bool, from_none], obj.get("isMinted"))
        is_listed = from_union([from_bool, from_none], obj.get("isListed"))
        mint_timestamp = from_union([from_int, from_none], obj.get("mintTimestamp"))
        expire_timestamp = from_union([from_int, from_none], obj.get("expireTimestamp"))
        return PrimarySale(order_id, id, list_timestamp, supply, price, is_minted, is_listed, mint_timestamp, expire_timestamp)

    def to_dict(self) -> dict:
        result: dict = {}
        result["orderId"] = from_none(self.order_id)
        result["_id"] = from_union([from_str, from_none], self.id)
        result["listTimestamp"] = from_union([from_int, from_none], self.list_timestamp)
        result["supply"] = from_union([from_int, from_none], self.supply)
        result["price"] = from_union([from_int, from_none], self.price)
        result["isMinted"] = from_union([from_bool, from_none], self.is_minted)
        result["isListed"] = from_union([from_bool, from_none], self.is_listed)
        result["mintTimestamp"] = from_union([from_int, from_none], self.mint_timestamp)
        result["expireTimestamp"] = from_union([from_int, from_none], self.expire_timestamp)
        return result


@dataclass
class Msrp:
    value: Optional[float] = None
    currency_symbol: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Msrp':
        assert isinstance(obj, dict)
        value = from_union([from_float, from_none], obj.get("value"))
        currency_symbol = from_union([from_str, from_none], obj.get("currencySymbol"))
        return Msrp(value, currency_symbol)

    def to_dict(self) -> dict:
        result: dict = {}
        result["value"] = from_union([to_float, from_none], self.value)
        result["currencySymbol"] = from_union([from_str, from_none], self.currency_symbol)
        return result


@dataclass
class TradeSettings:
    expire_time: Optional[int] = None
    sale_time: Optional[int] = None
    msrp: Optional[Msrp] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TradeSettings':
        assert isinstance(obj, dict)
        expire_time = from_union([from_int, from_none], obj.get("expireTime"))
        sale_time = from_union([from_int, from_none], obj.get("saleTime"))
        msrp = from_union([Msrp.from_dict, from_none], obj.get("msrp"))
        return TradeSettings(expire_time, sale_time, msrp)

    def to_dict(self) -> dict:
        result: dict = {}
        result["expireTime"] = from_union([from_int, from_none], self.expire_time)
        result["saleTime"] = from_union([from_int, from_none], self.sale_time)
        result["msrp"] = from_union([lambda x: to_class(Msrp, x), from_none], self.msrp)
        return result


@dataclass
class Nft:
    id: Optional[str] = None
    deactivated: Optional[bool] = None
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    media: Optional[Media] = None
    attributes: Optional[Attributes] = None
    symbol: Optional[str] = None
    markets: Optional[List[Market]] = None
    total_supply: Optional[int] = None
    mint: Optional[str] = None
    network: Optional[str] = None
    trade_settings: Optional[TradeSettings] = None
    updated_at: Optional[datetime] = None
    airdrops: Optional[List[Airdrop]] = None
    primary_sales: Optional[List[PrimarySale]] = None
    musician: Optional[str] = None
    created_at: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Nft':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        deactivated = from_union([from_bool, from_none], obj.get("deactivated"))
        name = from_union([from_str, from_none], obj.get("name"))
        description = from_union([from_str, from_none], obj.get("description"))
        image = from_union([from_str, from_none], obj.get("image"))
        media = from_union([Media.from_dict, from_none], obj.get("media"))
        attributes = from_union([Attributes.from_dict, from_none], obj.get("attributes"))
        symbol = from_union([from_str, from_none], obj.get("symbol"))
        markets = from_union([lambda x: from_list(Market.from_dict, x), from_none], obj.get("markets"))
        total_supply = from_union([from_int, from_none], obj.get("totalSupply"))
        mint = from_union([from_str, from_none], obj.get("mint"))
        network = from_union([from_str, from_none], obj.get("network"))
        trade_settings = from_union([TradeSettings.from_dict, from_none], obj.get("tradeSettings"))
        updated_at = from_union([from_datetime, from_none], obj.get("updatedAt"))
        airdrops = from_union([lambda x: from_list(Airdrop.from_dict, x), from_none], obj.get("airdrops"))
        primary_sales = from_union([lambda x: from_list(PrimarySale.from_dict, x), from_none], obj.get("primarySales"))
        musician = from_union([from_str, from_none], obj.get("musician"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        return Nft(id, deactivated, name, description, image, media, attributes, symbol, markets, total_supply, mint, network, trade_settings, updated_at, airdrops, primary_sales, musician, created_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["deactivated"] = from_union([from_bool, from_none], self.deactivated)
        result["name"] = from_union([from_str, from_none], self.name)
        result["description"] = from_union([from_str, from_none], self.description)
        result["image"] = from_union([from_str, from_none], self.image)
        result["media"] = from_union([lambda x: to_class(Media, x), from_none], self.media)
        result["attributes"] = from_union([lambda x: to_class(Attributes, x), from_none], self.attributes)
        result["symbol"] = from_union([from_str, from_none], self.symbol)
        result["markets"] = from_union([lambda x: from_list(lambda x: to_class(Market, x), x), from_none], self.markets)
        result["totalSupply"] = from_union([from_int, from_none], self.total_supply)
        result["mint"] = from_union([from_str, from_none], self.mint)
        result["network"] = from_union([from_str, from_none], self.network)
        result["tradeSettings"] = from_union([lambda x: to_class(TradeSettings, x), from_none], self.trade_settings)
        result["updatedAt"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        result["airdrops"] = from_union([lambda x: from_list(lambda x: to_class(Airdrop, x), x), from_none], self.airdrops)
        result["primarySales"] = from_union([lambda x: from_list(lambda x: to_class(PrimarySale, x), x), from_none], self.primary_sales)
        result["musician"] = from_union([from_str, from_none], self.musician)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        return result


def nfts_from_dict(s: Any) -> List[Nft]:
    return from_list(Nft.from_dict, s)


def nfts_to_dict(x: List[Nft]) -> Any:
    return from_list(lambda x: to_class(Nft, x), x)
