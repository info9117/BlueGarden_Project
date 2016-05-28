from behave import *
import re

@given('at the process page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    context.browser.get(context.address + '/process')
    assert "Add a new Process" in context.browser.page_source


@given('at the activity page for sathwick user')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    context.browser.get(context.address + '/activity')
    assert "Record Activity" in context.browser.page_source

@when('I select an exting process and add an activity')
def step_impl(context):
    addActivity(context, 'Dig a hole')

@when('a farmer creates a new process')
def step_impl(context):
    addProcess(context, "Grow Beef","The process by which grass becomes hamburgers")

@when('I select an exting process')
def step_impl(context):
    context.browser.get(context.address + '/activity/1/add')

@when('a farmer creates a new process with no name')
def step_impl(context):
    addProcess(context, "","The name of this process is classified")

@when('a farmer creates a new process with no description')
def step_impl(context):
    addProcess(context, "Null process","")


@then('I  will be directed to the Activity page and the process will be selected')
def step_impl(context):
    assert "Grow Spaghetti" in context.browser.page_source

@then('I will be shown the activity added to the process')
def step_impl(context):
    assert "Dig a hole" in context.browser.page_source

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

def addActivity(context, activity_description):
    context.browser.find_element_by_name('description').send_keys(activity_description)
    context.browser.find_element_by_id("form").submit()
