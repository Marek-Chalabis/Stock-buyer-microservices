from decimal import Decimal

import pytest

from src.utils.type_parsers import change_to_decimal


@pytest.mark.parametrize(
    ('tested_value', 'expected_value'),
    [
        ('100', Decimal(100)),
        ('+100', Decimal(100)),
        ('-100', -Decimal(100)),
        (100, Decimal(100)),
        (100.5, Decimal('100.5')),
        ('111,111,111', Decimal(111111111)),
        ('$1', Decimal(1)),
        ('-$1', -Decimal(1)),
        ('+$1', Decimal(1)),
    ],
)
def test_change_to_decimal(tested_value, expected_value):
    assert change_to_decimal(tested_value) == expected_value
