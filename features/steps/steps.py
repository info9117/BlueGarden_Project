from behave import *


@given('I am not currently logged in')
def step_impl(context):
    assert context.client


@when('I login with email and password')
def step_impl(context):
    context.page = context.client.post('/login', data=dict(
        email='singarisathwik007@gmail.com',
        password='dm08b048'
    ), follow_redirects=True)
    assert context.page


@then('I will be redirected to "My Dashboard"')
def step_impl(context):
    assert b'Hello Sathwik' in context.page.data


@when('I login with invalid email and password')
def step_impl(context):
    context.page = context.client.post('/login', data=dict(
        email='singarisathwik007@gmail.com',
        password='dm08b04'
    ), follow_redirects=True)
    assert context.page


@then('I will be shown error')
def step_impl(context):
    assert b'Email Id/Password do not match' in context.page.data


@given('I am not currently registered')
def step_impl(context):
    assert context.client


@when('I register with First name, Last name, Email Id & Password')
def step_impl(context):
    context.page = context.client.post('/register', data=dict(
                    firstname='Frodo',
                    lastname='Baggins',
                    email='fbaggins@lotr.com',
                    password='frodobaggins'),
                    follow_redirects=True)
    assert context.page


@then('I should be redirected to "My Dashboard"')
def step_impl(context):
    assert b'Hello Frodo' in context.page.data