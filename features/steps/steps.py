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

# begin of add_produce feature
@given('I am in the add produce page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    context.browser.get(context.address + '/farm/1/produce/add')
    assert 'Add Produce' in context.browser.page_source


@when(u'I enter the produce details')
def step_impl(context):
    add_produce(context, 'Eggplant', 'Bright Eggplants', 'Vegetable', '1', '4.32', '/eggplant.jpeg')
    assert context.browser.page_source


@then(u'I will receive a success message')
def step_impl(context):
    assert 'Success' in context.browser.page_source

# end of add_produce feature

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


def add_produce(context, name, description, category, units, price1, prod_image):
    name_field = context.browser.find_element_by_id("name")
    description_field = context.browser.find_element_by_id("description")
    name_field.send_keys(name)
    description_field.send_keys(description)
    context.browser.execute_script('$(function() { $("#category").val("'+category+'"); });')
    context.browser.execute_script('$(function() { $("#unit").val("'+units+'"); });')
    context.browser.execute_script('addItem()')
    price1_field = context.browser.find_element_by_id("price1")
    price1_field.send_keys(price1)
    context.browser.find_element_by_id("prod_image").send_keys(prod_image)
    name_field.submit()


