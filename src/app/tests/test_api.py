from service.entities import (
    DeliveryData,
    DeliveryResult,
    PostcodeInput,
    PostcodeOutput
)
from service.enums import Delivery
from service.exceptions import ServiceException

def test_calc__ok(client, mocker):

    #arrange
    check_result = DeliveryResult(   
        price=987.6,
        safe='hello world'
    )

    check_mock = mocker.patch(
        'service.main.DeliveryService.calc',
        return_value=check_result
    )

    #act
    response = client.post(
        path='/calc/',
        json={
            "name": Delivery.BX,
            "height": 123.1,
            "width": 234.2,
            "depth": 345.3,
            "weight": 15,
            "is_safe": True
        }
    )

    #assert
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.json['price'] == check_result['price']
    assert response.json['safe'] == check_result['safe']
    check_mock.assert_called_once_with(
        data=DeliveryData(
            name=Delivery.BX,
            height=123.1,
            width=234.2,
            depth=345.3,
            weight=15,
            is_safe=True
        )
    )

def test_calc__service_exception__internal_error(client, mocker):

    #arrange
    err_msg = '1234567'
    err_details = 'hello world'
    mocker.patch(
        'service.main.DeliveryService.calc',
        side_effect=ServiceException(
            message=err_msg,
            details=err_details
        )
    )

    #act
    response = client.post(
        path='/calc/',
        json={
            "name": Delivery.BX,
            "height": 123.1,
            "width": 234.2,
            "depth": 345.3,
            "weight": 15,
            "is_safe": True
        }
    )

    #assert
    assert response.status_code == 500
    assert response.content_type == 'application/json'
    assert response.json['error'] == err_msg
    assert response.json['details'] == err_details

def test_calc__validation_error__bad_request(
    client,
    mocker
):
    #arrange
    service_mock = mocker.patch('service.main.DeliveryService.calc')

    #act
    response = client.post(
        path='/calc/',
        json={
            "name": Delivery.BX,
            "height": 123.1,
            "width": 234.2,
            "depth": 345.3,
            "weight": 15
        }
    )

    #assert
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert response.json['error'] == 'ValidationError'
    assert response.json['details'] == {
        'is_safe': [
            "Missing data for required field."
        ]
    }
    service_mock.assert_not_called()   

def test_postcode__ok(client, mocker):

    #arrange
    postcode_result = PostcodeOutput(   
        full_address='ABOBA',
        postcode='assdas',
        timezone='12312312312'
    )

    postcode_mock = mocker.patch(
        'service.main.DeliveryService.postcode',
        return_value=postcode_result
    )

    #act
    response = client.post(
        path='/postcode/',
        json={
            "address": 'ABOBA'
        }
    )

    #assert
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.json['full_address'] == postcode_result['full_address']
    assert response.json['postcode'] == postcode_result['postcode']
    assert response.json['timezone'] == postcode_result['timezone']
    postcode_mock.assert_called_once_with(
        data=PostcodeInput(
            address='ABOBA'
        )
    )

def test_postcode__service_exception__internal_error(client, mocker):

    #arrange
    err_msg = '1234567'
    err_details = 'hello world'
    mocker.patch(
        'service.main.DeliveryService.postcode',
        side_effect=ServiceException(
            message=err_msg,
            details=err_details
        )
    )

    #act
    response = client.post(
        path='/postcode/',
        json={
            "address": "ABOBA" 
        }
    )

    #assert
    assert response.status_code == 500
    assert response.content_type == 'application/json'
    assert response.json['error'] == err_msg
    assert response.json['details'] == err_details

def test_postcode__validation_error__bad_request(
    client,
    mocker
):
    #arrange
    service_mock = mocker.patch('service.main.DeliveryService.postcode')

    #act
    response = client.post(
        path='/postcode/',
        json={
            "address": 12345
        }
    )

    #assert
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert response.json['error'] == 'ValidationError'
    assert response.json['details'] == {
        'address': [
            "Not a valid string."
        ]
    }
    service_mock.assert_not_called()   