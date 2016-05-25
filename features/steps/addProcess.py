from behave import *
import re

@given('at the process page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    context.browser.get(context.address + '/process')
    assert "Add a new Process" in context.browser.page_source

@when('a farmer creates a new process')
def step_impl(context):
    addProcess(context, "Grow Beef","The process by which grass becomes hamburgers")

@then('the new process is recorded')
def step_impl(context):
    assert 'Grow Beef'in context.browser.page_source

def login(context, email, password):
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()

def addProcess(context, process_name, process_description):
    context.browser.find_element_by_name('process_name').send_keys(process_name)
    context.browser.find_element_by_name('process_description').send_keys(process_description)
    context.browser.find_element_by_id("form").submit()
