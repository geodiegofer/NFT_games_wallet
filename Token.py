# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = tokens_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
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


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


@dataclass
class Context:
    slot: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Context':
        assert isinstance(obj, dict)
        slot = from_union([from_int, from_none], obj.get("slot"))
        return Context(slot)

    def to_dict(self) -> dict:
        result: dict = {}
        result["slot"] = from_union([from_int, from_none], self.slot)
        return result


@dataclass
class TokenAmount:
    amount: Optional[str] = None
    decimals: Optional[int] = None
    ui_amount: Optional[float] = None
    ui_amount_string: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TokenAmount':
        assert isinstance(obj, dict)
        amount = from_union([from_str, from_none], obj.get("amount"))
        decimals = from_union([from_int, from_none], obj.get("decimals"))
        ui_amount = from_union([from_float, from_none], obj.get("uiAmount"))
        ui_amount_string = from_union([from_str, from_none], obj.get("uiAmountString"))
        return TokenAmount(amount, decimals, ui_amount, ui_amount_string)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = from_union([from_str, from_none], self.amount)
        result["decimals"] = from_union([from_int, from_none], self.decimals)
        result["uiAmount"] = from_union([to_float, from_none], self.ui_amount)
        result["uiAmountString"] = from_union([from_str, from_none], self.ui_amount_string)
        return result


@dataclass
class Info:
    is_native: Optional[bool] = None
    mint: Optional[str] = None
    owner: Optional[str] = None
    state: Optional[str] = None
    token_amount: Optional[TokenAmount] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Info':
        assert isinstance(obj, dict)
        is_native = from_union([from_bool, from_none], obj.get("isNative"))
        mint = from_union([from_str, from_none], obj.get("mint"))
        owner = from_union([from_str, from_none], obj.get("owner"))
        state = from_union([from_str, from_none], obj.get("state"))
        token_amount = from_union([TokenAmount.from_dict, from_none], obj.get("tokenAmount"))
        return Info(is_native, mint, owner, state, token_amount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["isNative"] = from_union([from_bool, from_none], self.is_native)
        result["mint"] = from_union([from_str, from_none], self.mint)
        result["owner"] = from_union([from_str, from_none], self.owner)
        result["state"] = from_union([from_str, from_none], self.state)
        result["tokenAmount"] = from_union([lambda x: to_class(TokenAmount, x), from_none], self.token_amount)
        return result


@dataclass
class Parsed:
    info: Optional[Info] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Parsed':
        assert isinstance(obj, dict)
        info = from_union([Info.from_dict, from_none], obj.get("info"))
        type = from_union([from_str, from_none], obj.get("type"))
        return Parsed(info, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["info"] = from_union([lambda x: to_class(Info, x), from_none], self.info)
        result["type"] = from_union([from_str, from_none], self.type)
        return result


@dataclass
class Data:
    parsed: Optional[Parsed] = None
    program: Optional[str] = None
    space: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        parsed = from_union([Parsed.from_dict, from_none], obj.get("parsed"))
        program = from_union([from_str, from_none], obj.get("program"))
        space = from_union([from_int, from_none], obj.get("space"))
        return Data(parsed, program, space)

    def to_dict(self) -> dict:
        result: dict = {}
        result["parsed"] = from_union([lambda x: to_class(Parsed, x), from_none], self.parsed)
        result["program"] = from_union([from_str, from_none], self.program)
        result["space"] = from_union([from_int, from_none], self.space)
        return result


@dataclass
class Account:
    data: Optional[Data] = None
    executable: Optional[bool] = None
    lamports: Optional[int] = None
    owner: Optional[str] = None
    rent_epoch: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Account':
        assert isinstance(obj, dict)
        data = from_union([Data.from_dict, from_none], obj.get("data"))
        executable = from_union([from_bool, from_none], obj.get("executable"))
        lamports = from_union([from_int, from_none], obj.get("lamports"))
        owner = from_union([from_str, from_none], obj.get("owner"))
        rent_epoch = from_union([from_int, from_none], obj.get("rentEpoch"))
        return Account(data, executable, lamports, owner, rent_epoch)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([lambda x: to_class(Data, x), from_none], self.data)
        result["executable"] = from_union([from_bool, from_none], self.executable)
        result["lamports"] = from_union([from_int, from_none], self.lamports)
        result["owner"] = from_union([from_str, from_none], self.owner)
        result["rentEpoch"] = from_union([from_int, from_none], self.rent_epoch)
        return result


@dataclass
class Value:
    account: Optional[Account] = None
    pubkey: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Value':
        assert isinstance(obj, dict)
        account = from_union([Account.from_dict, from_none], obj.get("account"))
        pubkey = from_union([from_str, from_none], obj.get("pubkey"))
        return Value(account, pubkey)

    def to_dict(self) -> dict:
        result: dict = {}
        result["account"] = from_union([lambda x: to_class(Account, x), from_none], self.account)
        result["pubkey"] = from_union([from_str, from_none], self.pubkey)
        return result


@dataclass
class Result:
    context: Optional[Context] = None
    value: Optional[List[Value]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        assert isinstance(obj, dict)
        context = from_union([Context.from_dict, from_none], obj.get("context"))
        value = from_union([lambda x: from_list(Value.from_dict, x), from_none], obj.get("value"))
        return Result(context, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["context"] = from_union([lambda x: to_class(Context, x), from_none], self.context)
        result["value"] = from_union([lambda x: from_list(lambda x: to_class(Value, x), x), from_none], self.value)
        return result


@dataclass
class Tokens:
    jsonrpc: Optional[str] = None
    result: Optional[Result] = None
    id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Tokens':
        assert isinstance(obj, dict)
        jsonrpc = from_union([from_str, from_none], obj.get("jsonrpc"))
        result = from_union([Result.from_dict, from_none], obj.get("result"))
        id = from_union([from_int, from_none], obj.get("id"))
        return Tokens(jsonrpc, result, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["jsonrpc"] = from_union([from_str, from_none], self.jsonrpc)
        result["result"] = from_union([lambda x: to_class(Result, x), from_none], self.result)
        result["id"] = from_union([from_int, from_none], self.id)
        return result


def tokens_from_dict(s: Any) -> Tokens:
    return Tokens.from_dict(s)


def tokens_to_dict(x: Tokens) -> Any:
    return to_class(Tokens, x)
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = tokens_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
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


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


@dataclass
class Context:
    slot: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Context':
        assert isinstance(obj, dict)
        slot = from_union([from_int, from_none], obj.get("slot"))
        return Context(slot)

    def to_dict(self) -> dict:
        result: dict = {}
        result["slot"] = from_union([from_int, from_none], self.slot)
        return result


@dataclass
class TokenAmount:
    amount: Optional[str] = None
    decimals: Optional[int] = None
    ui_amount: Optional[float] = None
    ui_amount_string: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TokenAmount':
        assert isinstance(obj, dict)
        amount = from_union([from_str, from_none], obj.get("amount"))
        decimals = from_union([from_int, from_none], obj.get("decimals"))
        ui_amount = from_union([from_float, from_none], obj.get("uiAmount"))
        ui_amount_string = from_union([from_str, from_none], obj.get("uiAmountString"))
        return TokenAmount(amount, decimals, ui_amount, ui_amount_string)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = from_union([from_str, from_none], self.amount)
        result["decimals"] = from_union([from_int, from_none], self.decimals)
        result["uiAmount"] = from_union([to_float, from_none], self.ui_amount)
        result["uiAmountString"] = from_union([from_str, from_none], self.ui_amount_string)
        return result


@dataclass
class Info:
    is_native: Optional[bool] = None
    mint: Optional[str] = None
    owner: Optional[str] = None
    state: Optional[str] = None
    token_amount: Optional[TokenAmount] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Info':
        assert isinstance(obj, dict)
        is_native = from_union([from_bool, from_none], obj.get("isNative"))
        mint = from_union([from_str, from_none], obj.get("mint"))
        owner = from_union([from_str, from_none], obj.get("owner"))
        state = from_union([from_str, from_none], obj.get("state"))
        token_amount = from_union([TokenAmount.from_dict, from_none], obj.get("tokenAmount"))
        return Info(is_native, mint, owner, state, token_amount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["isNative"] = from_union([from_bool, from_none], self.is_native)
        result["mint"] = from_union([from_str, from_none], self.mint)
        result["owner"] = from_union([from_str, from_none], self.owner)
        result["state"] = from_union([from_str, from_none], self.state)
        result["tokenAmount"] = from_union([lambda x: to_class(TokenAmount, x), from_none], self.token_amount)
        return result


@dataclass
class Parsed:
    info: Optional[Info] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Parsed':
        assert isinstance(obj, dict)
        info = from_union([Info.from_dict, from_none], obj.get("info"))
        type = from_union([from_str, from_none], obj.get("type"))
        return Parsed(info, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["info"] = from_union([lambda x: to_class(Info, x), from_none], self.info)
        result["type"] = from_union([from_str, from_none], self.type)
        return result


@dataclass
class Data:
    parsed: Optional[Parsed] = None
    program: Optional[str] = None
    space: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        parsed = from_union([Parsed.from_dict, from_none], obj.get("parsed"))
        program = from_union([from_str, from_none], obj.get("program"))
        space = from_union([from_int, from_none], obj.get("space"))
        return Data(parsed, program, space)

    def to_dict(self) -> dict:
        result: dict = {}
        result["parsed"] = from_union([lambda x: to_class(Parsed, x), from_none], self.parsed)
        result["program"] = from_union([from_str, from_none], self.program)
        result["space"] = from_union([from_int, from_none], self.space)
        return result


@dataclass
class Account:
    data: Optional[Data] = None
    executable: Optional[bool] = None
    lamports: Optional[int] = None
    owner: Optional[str] = None
    rent_epoch: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Account':
        assert isinstance(obj, dict)
        data = from_union([Data.from_dict, from_none], obj.get("data"))
        executable = from_union([from_bool, from_none], obj.get("executable"))
        lamports = from_union([from_int, from_none], obj.get("lamports"))
        owner = from_union([from_str, from_none], obj.get("owner"))
        rent_epoch = from_union([from_int, from_none], obj.get("rentEpoch"))
        return Account(data, executable, lamports, owner, rent_epoch)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([lambda x: to_class(Data, x), from_none], self.data)
        result["executable"] = from_union([from_bool, from_none], self.executable)
        result["lamports"] = from_union([from_int, from_none], self.lamports)
        result["owner"] = from_union([from_str, from_none], self.owner)
        result["rentEpoch"] = from_union([from_int, from_none], self.rent_epoch)
        return result


@dataclass
class Value:
    account: Optional[Account] = None
    pubkey: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Value':
        assert isinstance(obj, dict)
        account = from_union([Account.from_dict, from_none], obj.get("account"))
        pubkey = from_union([from_str, from_none], obj.get("pubkey"))
        return Value(account, pubkey)

    def to_dict(self) -> dict:
        result: dict = {}
        result["account"] = from_union([lambda x: to_class(Account, x), from_none], self.account)
        result["pubkey"] = from_union([from_str, from_none], self.pubkey)
        return result


@dataclass
class Result:
    context: Optional[Context] = None
    value: Optional[List[Value]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        assert isinstance(obj, dict)
        context = from_union([Context.from_dict, from_none], obj.get("context"))
        value = from_union([lambda x: from_list(Value.from_dict, x), from_none], obj.get("value"))
        return Result(context, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["context"] = from_union([lambda x: to_class(Context, x), from_none], self.context)
        result["value"] = from_union([lambda x: from_list(lambda x: to_class(Value, x), x), from_none], self.value)
        return result


@dataclass
class Tokens:
    jsonrpc: Optional[str] = None
    result: Optional[Result] = None
    id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Tokens':
        assert isinstance(obj, dict)
        jsonrpc = from_union([from_str, from_none], obj.get("jsonrpc"))
        result = from_union([Result.from_dict, from_none], obj.get("result"))
        id = from_union([from_int, from_none], obj.get("id"))
        return Tokens(jsonrpc, result, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["jsonrpc"] = from_union([from_str, from_none], self.jsonrpc)
        result["result"] = from_union([lambda x: to_class(Result, x), from_none], self.result)
        result["id"] = from_union([from_int, from_none], self.id)
        return result


def tokens_from_dict(s: Any) -> Tokens:
    return Tokens.from_dict(s)


def tokens_to_dict(x: Tokens) -> Any:
    return to_class(Tokens, x)
