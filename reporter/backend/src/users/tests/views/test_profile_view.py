from decimal import Decimal

import pytest

from flask_login import login_user

from src.users.enums import MoneyOperation
from src.users.view import (
    ProfileView,
    RegisterView,
)


class TestProfileView:
    def test_view_methods(self):
        assert RegisterView.methods == ['GET', 'POST']

    def test_dispatch_request_handle_money_form(self, mocker):
        mocker_money_form = mocker.patch('src.users.view.MoneyForm')
        mocker_form = mocker.Mock(
            submit_money=mocker.Mock(data=True),
            validate_on_submit=mocker.Mock(return_value=True),
        )
        mocker_money_form.return_value = mocker_form
        mocker_handle_money_form = mocker.patch(
            'src.users.view.ProfileView._handle_money_form',
        )
        ProfileView().dispatch_request()
        mocker_handle_money_form.assert_called_once_with()

    def test_dispatch_request_render_template(self, mocker):
        mocker_money_form = mocker.patch('src.users.view.MoneyForm')
        mocker_form = mocker.Mock(submit_money=mocker.Mock(data=False))
        mocker_money_form.return_value = mocker_form
        mocker_render_template = mocker.patch('src.users.view.render_template')
        ProfileView().dispatch_request()
        mocker_render_template.assert_called_once_with(
            template_name_or_list='profile.html',
            money_form=mocker_form,
        )

    @pytest.mark.parametrize(
        ('tested_amount', 'expected_amount'),
        [
            (Decimal(10), '10'),
            (Decimal(-10), '-10'),
        ],
    )
    def test_handle_money_form_form_valid(
        self,
        mocker,
        user_in_db,
        tested_amount,
        expected_amount,
    ):
        login_user(user_in_db)
        mocker_money_form = mocker.patch('src.users.view.MoneyForm')
        mocker_form = mocker.Mock(
            validate_on_submit=mocker.Mock(return_value=True),
            amount=mocker.Mock(data=tested_amount),
            operation=mocker.Mock(data=MoneyOperation.DEPOSIT),
        )
        mocker_money_form.return_value = mocker_form
        mocker_update_money_by_amount = mocker.patch(
            'src.users.models.UserProfile.update_money_by_amount',
        )
        ProfileView()._handle_money_form()
        mocker_update_money_by_amount.assert_called_once_with(
            amount=expected_amount,
            commit=True,
        )

    def test_handle_money_form_form_valid_flash(self, mocker, user_in_db):
        login_user(user_in_db)
        mocker_money_form = mocker.patch('src.users.view.MoneyForm')
        mocker_form = mocker.Mock(
            validate_on_submit=mocker.Mock(return_value=True),
        )
        mocker_money_form.return_value = mocker_form
        mocker.patch('src.users.models.UserProfile.update_money_by_amount')
        mocker_flash = mocker.patch('src.users.view.flash')
        ProfileView()._handle_money_form()
        mocker_flash.assert_called_once()

    def test_handle_money_form_form_invalid(self, mocker):
        mocker_money_form = mocker.patch('src.users.view.MoneyForm')
        mocker_form = mocker.Mock(
            validate_on_submit=mocker.Mock(return_value=False),
        )
        mocker_money_form.return_value = mocker_form
        mocker_flash_errors_from_form = mocker.patch(
            'src.users.view.flash_errors_from_form',
        )
        ProfileView()._handle_money_form()
        mocker_flash_errors_from_form.assert_called_once_with(form=mocker_form)
