from behave import *
import re


@given('I am logged in as a manager')
def step_impl(context):
    login(context, 'admin@gmail.com', 'pswd1234')
    assert context.browser.page_source


@when('I open feedback management portal')
def step_impl(context):
    context.browser.get(context.address + '/feedbackmgmt')
    assert 'Welcome. Manager.'


@then('system should display all received feedback, including <name>, <email>, <title>, <enquiry>')
def step_impl(context):
    contact(context, name='Fate', email='fate@microsoft.com', title='Hey!', enquiry='I am not happy. -_-##')


def login(context, email, password):
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()


def contact(context, name, email, title, enquiry):
    name_field = context.browser.find_element_by_id("name")
    email_field = context.browser.find_element_by_id("email")
    title_field = context.browser.find_element_by_id("title")
    enquiry_field = context.browser.find_element_by_id("enquiry")
    name_field.send_keys(name)
    email_field.send_keys(email)
    title_field.send_keys(title)
    enquiry_field.send_keys(enquiry)
    email_field.submit()


