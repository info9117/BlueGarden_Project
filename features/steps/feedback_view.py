from behave import *
import re


@given('I am logged in to system')
def step_impl(context):
    login(context, 'admin@gmail.com', 'dm08b04')
    assert context.browser.page_source


@when('I open feedback management portal')
def step_impl(context):
    context.browser.get(context.address + '/feedbackmgmt')
    assert 'Welcome. Admin.'


@then('system should display all received feedback')
def step_impl(context):
    contact(context, )


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

def contact(context, name, email, title, enquiry):
    name_field = context.browser.find_element_by_id("name")
    email_field = context.browser.find_element_by_id("email")
    title_field = context.browser.find_element_by_id("title")
    enquiry_field = context.browser.find_element_by_id("enquiry")
    name_field.send_keys(name)
    email_field.send_keys(email)
    title_field.send_keys(title)
    enquiry_field.send_keys(enquiry)


