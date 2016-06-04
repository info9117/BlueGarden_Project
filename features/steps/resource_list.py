from behave import *
import re

@given('at the add resource page')
def step_impl(context):
    context.browser.get(context.address + '/login')
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    context.browser.get(context.address + '/addresource')
    assert 'Add Resource' in context.browser.page_source

@when('a user input the resource decription')
def step_impl(context):
    add_resource(context,'this is you resource')
    assert context.browser.page_source

@then('he can add this resource to the resource list')
def step_impl(context):
    #return True
    assert 'this is you resource' in context.browser.page_source


def add_resource(context, description):
    description_field = context.browser.find_element_by_id("resourcedescription")
    description_field.send_keys(description)
    description_field.submit()


def login(context, email, password):
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()