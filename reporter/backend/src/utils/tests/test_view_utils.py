from unittest.mock import call

from src.utils.view_utils import flash_errors_from_form


def test_flash_errors_from_form(mocker):
    mocker_flash = mocker.patch('src.utils.view_utils.flash')
    tested_form = mocker.patch('src.utils.view_utils.FlaskForm')
    tested_form.errors = {
        'test_error1': ['test_error1'],
        'test_error2': ['test_error2'],
    }

    flash_errors_from_form(tested_form)
    mocker_flash.assert_has_calls(
        [
            call('test_error1', category='danger'),
            call('test_error2', category='danger'),
        ],
    )
