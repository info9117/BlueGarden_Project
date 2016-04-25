from behave import *
import re


@given('I am in the login page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login_found = re.search("LOGIN", context.browser.page_source)
    assert login_found


@when('I login with email and password')
def step_impl(context):
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    assert context.browser.page_source


@then('I will be redirected to "My Dashboard"')
def step_impl(context):
    context.browser.get(context.address + "/dashboard")
    assert 'Hello Sathwik' in context.browser.page_source


@when('I login with invalid email and password')
def step_impl(context):
    login(context, 'singarisathwik007@gmail.com', 'dm08b04')
    assert context.browser.page_source


@then('I will be shown error')
def step_impl(context):
    assert 'Email Id/Password do not match' in context.browser.page_source


@given('I am in registration page')
def step_impl(context):
    context.browser.get(context.address + "/register")
    register_found = re.search("REGISTER", context.browser.page_source)
    assert register_found


@when('I register with First name, Last name, Email Id & Password')
def step_impl(context):
    register(context,  first_name='Frodo', last_name='Baggins', email='fbaggins@lotr.com', password='frodobaggins')
    assert context.browser.page_source


@then('I should be redirected to "My Dashboard"')
def step_impl(context):
    context.browser.get(context.address + "/dashboard")
    assert 'Hello Frodo' in context.browser.page_source


@when('I register with First name, Last name, existing Email Id & Password')
def step_impl(context):
    register(context, first_name='Frodo', last_name='Baggins', email='fbaggins@lotr.com', password='frodobaggins')
    assert context.browser.page_source


@then('I should be shown error')
def step_impl(context):
    assert 'Email Id already exists' in context.browser.page_source



    

def login(context, email, password):
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()


def register(context, first_name, last_name, email, password):
    firstname_field = context.browser.find_element_by_id("firstname")
    lastname_field = context.browser.find_element_by_id("lastname")
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    firstname_field.send_keys(first_name)
    lastname_field.send_keys(last_name)
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()
    

    