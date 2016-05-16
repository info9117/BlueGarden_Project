from behave import *
import re
from models import *

@given('user is in contact form page')
def step_impl(context):
    context.browser.get(context.address + "/contact")
    contact_found = re.search("CONTACT", context.browser.page_source)
    assert contact_found


@when('user fills the form without title')
def step_impl(context):
    contact(context, 'singarisathwik007@gmail.com', 'dm08b048')
    assert context.browser.page_source


@then('system should show an error')
def step_impl(context):
    context.browser.get(context.address + "/dashboard")
    assert 'Hello Sathwik' in context.browser.page_source


def contact(context, email, enquiry):
    email_field = context.browser.find_element_by_id("email")
    enquiry_field = context.browser.find_element_by_id("enquiry")
    email_field.send_keys(email)
    enquiry_field.send_keys(enquiry)
    email_field.submit()