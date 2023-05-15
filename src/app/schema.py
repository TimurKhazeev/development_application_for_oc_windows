from marshmallow import Schema, validate
from marshmallow.fields import (
    Integer,
    Float,
    String,
    Boolean,
    Method
)

from marshmallow.decorators import (
    post_load
)

from service.entities import (
    DeliveryData, 
    DeliveryResult,
    PostcodeInput,
    PostcodeOutput
)

from service.enums import Delivery


class CalcSchema(Schema):

    name = String(
        load_only=True,
        required=True,
        # validate=validate.OneOf(Delivery.VALUES)
    )
    height = Float(
        load_only=True,
        required=True
    )
    width = Float(
        load_only=True,
        required=True
    )
    depth = Float(
        load_only=True,
        required=True
    )
    weight = Integer(
        load_only=True,
        required=True
    )    
    is_safe = Boolean(
        load_only=True,
        required=True
    )

    price = Float(dump_only=True)
    safe = String(dump_only=True)

    @post_load
    def make_calc_data(self, data, **kwargs):
        return DeliveryData(**data)


class PostcodeSchema(Schema):

    address = String(
        load_only=True,
        required=True,
    )
    full_address = String(dump_only=True)
    postcode = String(dump_only=True)
    timezone = String(dump_only=True)

    @post_load
    def make_postcode_data(self, data, **kwargs):
        return PostcodeInput(**data)


class BadRequestSchema(Schema):

    error = Method('dump_error')
    details = Method("dump_details")

    def dump_error(self, obj):
        return "ValidationError"
    
    def dump_details(self, obj):
        return obj.description.messages


class ServiceExceptionSchema(Schema):

    error = Method('dump_error')
    details = Method("dump_details")

    def dump_error(self, obj):
        # return "ServiceException"
        return obj.description.message
     
    def dump_details(self, obj):
        return obj.description.details
        # return "Some details"