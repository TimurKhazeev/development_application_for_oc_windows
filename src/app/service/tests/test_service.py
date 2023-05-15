import pytest
from service.main import (
    BaseDeliveryService,
    InternationalService,
    DomesticService,
    DeliveryService
)
from service.enums import Delivery
from service.entities import (
    DeliveryData,
    DeliveryResult,
    PostcodeInput,
    PostcodeOutput
)
from service.exceptions import (
    DeliveryException,
    DadataException
)
from service import messages

class TestDeliveryService:

    @pytest.mark.parametrize('name', Delivery.INTERNATIONAL)
    def test_calc__call_international_service__ok(
        self,
        name,
        mocker):
        
        # arrange
        check_input = DeliveryData(
            name=name,
            height=123.1,
            width=234.2,
            depth=345.3,
            weight=456,
            is_safe=True
        )

        check_result = DeliveryResult(   
            price=567.4,
            safe='some code'
        )

        calc_delivery_mock = mocker.patch(
            'service.main.InternationalService.calc_delivery',
            return_value=check_result
        )

        service =  DeliveryService()

        #act
        result = service.calc(data=check_input)

        #assert
        calc_delivery_mock.assert_called_once_with(check_input)
        assert result == check_result


    @pytest.mark.parametrize('name', Delivery.DOMESTIC)
    def test_calc__call_domestic_service__ok(
        self,
        name,
        mocker):
        
        # arrange
        check_input = DeliveryData(
            name=name,
            height=123.1,
            width=234.2,
            depth=345.3,
            weight=456,
            is_safe=True
        )

        check_result = DeliveryResult(   
            price=567.4,
            safe='some code'
        )

        calc_delivery_mock = mocker.patch(
            'service.main.DomesticService.calc_delivery',
            return_value=check_result
        )

        service =  DeliveryService()

        #act
        result = service.calc(data=check_input)

        #assert
        calc_delivery_mock.assert_called_once_with(check_input)
        assert result == check_result

    def test_calc__invalid_delivery__raise_exception(self):

        # arrange
        check_input = DeliveryData(
            name='WB',
            height=123.1,
            width=234.2,
            depth=345.3,
            weight=456,
            is_safe=True
        )

        #act
        with pytest.raises(DeliveryException) as ex:
            DeliveryService().calc(data=check_input)

        #assert
        assert ex.value.message == messages.MSG_1

class TestDomesticService:

    def test_calc_delivery__calc_delivery__ok(self,mocker):

        #arrange
        check_input = DeliveryData(
            name=Delivery.PR,
            height=123.1,
            width=234.2,
            depth=345.3,
            weight=456,
            is_safe=True
        )

        check_result = DeliveryResult(
            price=567.4,
            safe="Hello World"
        )

        check_safe_mock = mocker.patch(
            'service.main.DomesticService.check_safe',
            return_value=check_result
        )

        service = DomesticService()
        
        #act
        result = service.calc_delivery(data=check_input)

        #assert
        check_safe_mock.assert_called_once_with(
            price=10,
            is_safe=False
        )
        assert result == check_result
