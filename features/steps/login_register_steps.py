from behave import *
from features.steps import login, register


@given("I am at the login page")
def step_impl(context):
    context.browser.get(context.address + "/login")
    assert "login" in context.browser.page_source


@when('I login with "{email}" and "{password}"')
def step_impl(context, email, password):
    login(context, email, password)
    assert context.browser.page_source


@given("I am at the registration page")
def step_impl(context):
    context.browser.get(context.address + "/register")
    assert "register" in context.browser.page_source


@when('I register as "{first_name}", "{last_name}", "{email}", "{password}" & "{confirm_password}"')
def step_impl(context, first_name, last_name, email, password, confirm_password):
    register(context, first_name, last_name, email, password, confirm_password)
    assert context.browser.page_source
