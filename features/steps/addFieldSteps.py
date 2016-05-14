from behave import *
import re

@given('at the field page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    context.browser.get(context.address + '/field')
    assert "Add a Field" in context.browser.page_source

@when('a farmer submits new field name and valid farm name')
def step_impl(context):
    addTestField(context, "Addison Field","Shire Farms" )

@then('the new field name is recorded with the parent farm')
def step_impl(context):
    assert 'Addison Field'in context.browser.page_source
    #assert 'not your farm'in context.browser.page_source


def login(context, email, password):
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()

def addTestField(context, fieldName, farmName):
    context.browser.find_element_by_name('fieldname').send_keys(fieldName)
    context.browser.find_element_by_name('farmname').send_keys(farmName)
    context.browser.find_element_by_id("form").submit()