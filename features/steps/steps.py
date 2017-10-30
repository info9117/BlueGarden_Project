import time
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


@when('I register with First name, Last name, Email Id , Password & ConfirmPassword')
def step_impl(context):
    register(context, first_name='Frodo', last_name='Baggins', email='fbaggins@lotr.com', password='frodobaggins',
             confirmpassword='frodobaggins')
    assert context.browser.page_source


@then('I should be redirected to "My Dashboard"')
def step_impl(context):
    context.browser.get(context.address + "/dashboard")
    assert 'Hello Frodo' in context.browser.page_source


@when('I register with First name, Last name, existing Email Id , Password & ConfirmPassword')
def step_impl(context):
    register(context, first_name='Frodo', last_name='Baggins', email='fbaggins@lotr.com', password='frodobaggins',
             confirmpassword='frodobaggins')
    assert context.browser.page_source


@then('I should be shown error')
def step_impl(context):
    assert 'Email Id already exists' in context.browser.page_source


# begin of add_produce feature

@when(
    'I register with First name, Last name, Email Id , Password & ConfirmPassword(Password and ConfirmPassword is not equal)')
def step_impl(context):
    register(context, first_name='Frodo', last_name='Baggins', email='fbaggins@lotr.com', password='frodobaggins',
             confirmpassword='fefefefe')
    assert context.browser.page_source


@then('I should be shown the error')
def step_impl(context):
    assert 'Password and ConfirmPassword is not equal' in context.browser.page_source


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
    time.sleep(3)
    assert 'You successfully added Eggplant' in context.browser.page_source


# end of add_produce feature

@given(u'I am logged in at the dashboard page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    assert 'Hello Sathwik' in context.browser.page_source


@then(u'I will see the most recently viewed produce')
def step_impl(context):
    assert 'corn' in context.browser.page_source


@given(u'I am at home page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    assert 'Hello Sathwik' in context.browser.page_source


@when(u'I go to browse produce page')
def step_impl(context):
    context.browser.get(context.address + '/farm/1/produce/add')
    add_produce(context, 'Eggplant', 'Bright Eggplants', 'Vegetable', '1', '4.32', '/eggplant.jpeg')
    context.browser.get(context.address + "/search/produce")
    assert 'Browse Produce' in context.browser.page_source


@when(u'I go to browse produce page and apply filters')
def step_impl(context):
    context.browser.get(context.address + '/farm/1/produce/add')
    add_produce(context, 'Corn', 'Amazing Corn', 'Vegetable', '1', '2.25', '/eggplant.jpeg')
    context.browser.get(context.address + "/search/produce?search=Cor&location=sydney")
    assert True


@then(u'I see produce in the page')
def step_impl(context):
    assert 'Eggplant' in context.browser.page_source


@then(u'I see filtered produce in the page')
def step_impl(context):
    assert 'Corn' in context.browser.page_source


def login(context, email, password):
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()


def register(context, first_name, last_name, email, password, confirmpassword):
    firstname_field = context.browser.find_element_by_id("firstname")
    lastname_field = context.browser.find_element_by_id("lastname")
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    confirmpassword_field = context.browser.find_element_by_id("confirmpassword")
    firstname_field.send_keys(first_name)
    lastname_field.send_keys(last_name)
    email_field.send_keys(email)
    password_field.send_keys(password)
    confirmpassword_field.send_keys(confirmpassword)
    email_field.submit()


def add_produce(context, name, description, category, units, price1, prod_image):
    name_field = context.browser.find_element_by_id("name")
    description_field = context.browser.find_element_by_id("description")
    name_field.send_keys(name)
    description_field.send_keys(description)
    context.browser.execute_script('$(function() { $("#category").val("' + category + '"); });')
    context.browser.execute_script('$(function() { $("#unit").val("' + units + '"); });')
    context.browser.execute_script('addItem()')
    price1_field = context.browser.find_element_by_id("price1")
    price1_field.send_keys(price1)
    context.browser.find_element_by_id("prod_image").send_keys(prod_image)
    name_field.submit()


@given('at the product details page')
def step_impl(context):
    context.browser.get(context.address + "/produce/1")


@given(u'the product details page and produce price')
def step_impl(context):
    context.browser.get(context.address + "/produce/1")


@then('the system shows product details product name, farm name, price, unit and image')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.page_source


@when(u'the user selects the {amount} of the product')
def step_impl(context, amount):
    """
    :type context:  behave,runner.context
    :type amount: int
    """
    amount_field = context.browser.find_element_by_id("amount")
    amount_field.send_keys(str(amount))
    amount_field.submit()


@then(u'the system shows the total is {total}')
def step_impl(context, total):
    """
    :type context:  behave,runner.context
    :type total: float
    """
    assert str(total) in context.browser.page_source


def send_feedback(context, username, email, subject, message):
    username_field = context.browser.find_element_by_id("username")
    email_field = context.browser.find_element_by_id("email")
    subject_field = context.browser.find_element_by_id("subject")
    message_field = context.browser.find_element_by_id("message")
    username_field.send_keys(username)
    email_field.send_keys(email)
    subject_field.send_keys(subject)
    message_field.send_keys(message)
    email_field.submit()


@given('I am in feedback page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')

    context.browser.get(context.address + "/feedback")
    register_found = re.search("feedback", context.browser.page_source)
    assert register_found


@when('I register with User name, Email, Subject, Message')
def step_impl(context):
    send_feedback(context, username='sam', email='example@gmail.com', subject="feedback", message='Hello!')
    assert context.browser.page_source


@then('I should be shown thank message')
def step_impl(context):
    assert 'thank' in context.browser.page_source


@given(u'I am in purchase page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    context.browser.get(context.address + "/purchase")
    assert 'Amount:' in context.browser.page_source


@when(u'I click the payment button')
def step_impl(context):
    time.sleep(5)
    context.browser.execute_script('$(".stripe-button").click();')
    time.sleep(5)
    assert True


@then(u'I can enter my credit card details to pay')
def step_impl(context):
    time.sleep(5)
    context.browser.execute_script('$("#email").val( "jbhewitt12@gmail.com" );')
    context.browser.execute_script('$("#card_number").val( "4242424242424242" );')
    context.browser.execute_script('$("#cc-exp").val( "1122" );')
    context.browser.execute_script('$("#cc-csc").val( "2222" );')
    context.browser.execute_script('$("#submitButton").click();')
    assert True


@given(u'the user at the checkout page')
def step_impl(context):
    context.browser.get(context.address + "/checkout/1")


@when(u'the user enters his {name} {email} {phone} {address} {discount} and clicks on save buyer info')
def step_impl(context, name, email, phone, address, discount):
    """
    :type context:  behave,runner.context
    :type name: str
    :type email: str
    :type phone: int
    :type address: str
    :type discount: int
    """
    name_field = context.browser.find_element_by_id("name")
    name_field.send_keys(str(name))
    email_field = context.browser.find_element_by_id("email")
    email_field.send_keys(str(email))
    phone_field = context.browser.find_element_by_id("phone")
    phone_field.send_keys(str(phone))
    address_field = context.browser.find_element_by_id("address")
    address_field.send_keys(str(address))
    discount_field = context.browser.find_element_by_id("discount")
    discount_field.send_keys(str(discount))
    name_field.submit()


@then(
    u'the system saves the information into the database and shows success message to the user and total value of item and total value after discount')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert "information has been saved successfully" in context.browser.page_source


def send_feedback(context, username, email, subject, message):
    username_field = context.browser.find_element_by_id("username")
    email_field = context.browser.find_element_by_id("email")
    subject_field = context.browser.find_element_by_id("subject")
    message_field = context.browser.find_element_by_id("message")
    username_field.send_keys(username)
    email_field.send_keys(email)
    subject_field.send_keys(subject)
    message_field.send_keys(message)
    email_field.submit()
