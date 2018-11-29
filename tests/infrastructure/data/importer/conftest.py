from pytest import fixture
from json import dump
from authark.application.repositories import (
    ExpressionParser, MemoryUserRepository)


@fixture
def user_repository():
    user_repository = MemoryUserRepository(ExpressionParser)
    return user_repository


@fixture(scope='session')
def import_users():
    return [
        {
            "name": "Bryan Jackson",
            "external_id": 1232,
            "email": "chaikin@hotmail.com",
            "external_source": "erp.users",
            "gender": "male",
            "birthdate": "",
            "phone_number": "3234444176",
            "address": "Garden Avenue",
            "attributes": {
                "partner_id": 37679,
                "employee_id": ""
            }
        },
        {
            "name": "Bronwyn Everett",
            "external_id": 1915,
            "email": "padme@gmail.com",
            "external_source": "erp.users",
            "gender": "male",
            "birthdate": "",
            "phone_number": "",
            "address": "Craigmore Avenue 55 - 24",
            "attributes": {
                "partner_id": 43984,
                "employee_id": ""
            }
        },
        {
            "name": "Inara White",
            "external_id": 319,
            "email": "arandal@verizon.net",
            "external_source": "erp.users",
            "gender": "female",
            "birthdate": "1984-08-27",
            "phone_number": "3238925176",
            "address": "Laurel Terrace 66 - 123",
            "attributes": {
                "partner_id": 43984,
                "employee_id": 7910
            }
        },
        {
            "name": "Athena Miller",
            "external_id": 2199,
            "email": "punkis@outlook.com",
            "external_source": "erp.users",
            "gender": "male",
            "birthdate": "1969-09-17",
            "phone_number": "3177735591",
            "address": "Seymour Street",
            "attributes": {
                "partner_id": 7507,
                "employee_id": 4674
            }
        },
        {
            "name": "Zayn Finnegan",
            "external_id": 2200,
            "email": "sjmuir@me.com",
            "external_source": "erp.users",
            "gender": "male",
            "birthdate": "1963-03-04",
            "phone_number": "3117267860",
            "address": "Elstree Gardens",
            "attributes": {
                "partner_id": 8393,
                "employee_id": 5365
            }
        }
    ]
