from behave import *
import re


@given('user is in contact form page')
def step_impl(context):
    context.browser.get(context.address + "/contact")
    contact_found = re.search("CONTACT", context.browser.page_source)
    assert contact_found


@when('user fills the form without title')
def step_impl(context):
    contact(context, '', 'I have something to say! >_<', 'test@test.com')
    assert context.browser.page_source


@then('system should show an error to ask user fill title')
def step_impl(context):
    assert 'You need to enter a title.' in context.browser.page_source



@when('user fills the form without body')
def step_impl(context):
    contact(context, 'Hey!', '', 'test@test.com')
    assert context.browser.page_source


@then('system should show an error to ask user fill body')
def step_impl(context):
    assert 'You need to tell us more.' in context.browser.page_source


@when('user fills the form without email address')
def step_impl(context):
    contact(context, 'Hey!', 'I have something to say! >_<', '')
    assert context.browser.page_source


@then('system should show a warning')
def step_impl(context):
    assert 'We will not be able to tell you what we think. >_<' in context.browser.page_source


def contact(context, title, enquiry, email):
    email_field = context.browser.find_element_by_id("email")
    enquiry_field = context.browser.find_element_by_id("enquiry")
    title_field = context.browser.find_element_by_id("title")
    email_field.send_keys(email)
    enquiry_field.send_keys(enquiry)
    title_field.send_keys(title)
    # email_field.submit() # what does this mean?