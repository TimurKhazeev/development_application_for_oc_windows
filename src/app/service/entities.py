from typing_extensions import TypedDict


class DeliveryData(TypedDict):

    name: str
    height: float
    width: float
    depth: float
    weight: int
    is_safe: bool


class DeliveryResult(TypedDict):

    price: float
    safe: str

class PostcodeInput(TypedDict):

    address: str

class PostcodeOutput(TypedDict):

    full_address: str
    postcode: str
    timezone: str