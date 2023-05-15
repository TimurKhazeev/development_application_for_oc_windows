from abc import ABC, abstractmethod
from dadata import Dadata
from service.entities import (
    DeliveryData,
    DeliveryResult,
    PostcodeInput,
    PostcodeOutput
)
from service.enums import Delivery
from service.keys import API_KEY, SECRET_KEY
from service import exceptions

import httpx


class BaseDeliveryService(ABC):

    @abstractmethod
    def calc_delivery(self, data: DeliveryData) -> DeliveryResult:
        pass


class InternationalService(BaseDeliveryService):

    def calc_delivery(self, data: DeliveryData) -> DeliveryResult:

        h: float = data["height"]
        w: float = data["width"]
        d: float = data["depth"]
        weight: int = data["weight"]
        is_safe: bool = data["is_safe"]

        price = h * w * d * weight * 0.5
        if (is_safe):
            price = price*2
            is_safe = "Застраховано"
        else:
            is_safe = "Отказано в страховке"
        return DeliveryResult(
                price=price,
                safe=is_safe
            )


class DomesticService(BaseDeliveryService):

    def check_safe(self, price: float, is_safe:bool) -> DeliveryResult:

        safe="Застраховано" if is_safe else "Отказано в страховке"
        
        return DeliveryResult(
            price=price,
            safe=safe
        )

    def calc_delivery(self, data: DeliveryData) -> DeliveryResult:

        h: float = data["height"]
        w: float = data["width"]
        d: float = data["depth"]
        weight: int = data["weight"]
        is_safe: bool = data["is_safe"]

        price = h * w * d * weight * 0.5
        
        return self.check_safe(price, is_safe)


class DeliveryService:

    def calc(self, data: DeliveryData):

        name: str = data['name']

        if name in Delivery.INTERNATIONAL:
            service = InternationalService()
        elif name in Delivery.DOMESTIC:
            service = DomesticService()
        else:
            raise exceptions.DeliveryException()

        return service.calc_delivery(data)

    def postcode(self, data: PostcodeInput):

        address: str = data["address"]
        dadata = Dadata(API_KEY, SECRET_KEY)
        try:
            result = dadata.clean(name="address", source=address)
        except (httpx.ConnectError) as ex:
            raise exceptions.DadataException(details=str(ex))
        else:
            return PostcodeOutput(
                full_address=result["result"],
                postcode=result["postal_code"],
                timezone=result["timezone"]
            )
