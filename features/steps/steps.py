from behave import *
import re

@given('at the product details page')
def step_impl(context):
    context.browser.get(context.address + "/produce/1")



@then('the system shows product details product name, farm name, price, unit and image')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

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
    register(context,  first_name='Frodo', last_name='Baggins', email='fbaggins@lotr.com', password='frodobaggins', confirmpassword='frodobaggins')
    assert context.browser.page_source


@then('I should be redirected to "My Dashboard"')
def step_impl(context):
    context.browser.get(context.address + "/dashboard")
    assert 'Hello Frodo' in context.browser.page_source


@when('I register with First name, Last name, existing Email Id , Password & ConfirmPassword')
def step_impl(context):
    register(context, first_name='Frodo', last_name='Baggins', email='fbaggins@lotr.com', password='frodobaggins',confirmpassword='frodobaggins')
    assert context.browser.page_source


@then('I should be shown error')
def step_impl(context):
    assert 'Email Id already exists' in context.browser.page_source

<<<<<<< HEAD
# begin of add_produce feature
=======
@when('I register with First name, Last name, Email Id , Password & ConfirmPassword(Password and ConfirmPassword is not equal)')
def step_impl(context):
    register(context, first_name='Frodo', last_name='Baggins', email='fbaggins@lotr.com', password='frodobaggins',confirmpassword='fefefefe')
    assert context.browser.page_source

@then('I should be shown the error')
def step_impl(context):
    assert 'Password and ConfirmPassword is not equal' in context.browser.page_source

>>>>>>> sprint-3-nanoha
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


@then(u'I see produce in the page')
def step_impl(context):
    assert 'Eggplant' in context.browser.page_source



def login(context, email, password):
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()


def register(context, first_name, last_name, email, password,confirmpassword):
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


@given(u'the product details page and produce price')
def step_impl(context):
    context.browser.get(context.address + "/produce/1")


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




