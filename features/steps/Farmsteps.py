from behave import *
import re

@given('at the sell page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'farmer_j01@gmail.com', 'louise1993')
    context.browser.get(context.address + "/sell")
    assert 'Add Farm' in context.browser.page_source

@when('a farmer submits valid farm name and address')
def step_impl(context):
    add_farm(context, "Marrickville Community Garden", "1 Marry St", "", "Marickville", "NSW", "Australia", "2009")



@then('the new farm name is displayed in the My Farms list')
def step_impl(context):
    assert 'Marrickville Community Garden' in context.browser.page_source

@given('logged in at the sell page')
def step_impl(context):
    assert True

@when('a farmer submits an invalid (already existing) farm name')
def step_impl(context):
    add_farm(context, "Marrickville Community Garden", "1 Marry St", "", "Marickville", "NSW", "Australia", "2009")

@then('the the error: "Already Exists" is returned')
def step_impl(context):
    assert 'Already Exists' in context.browser.page_source
    
@given('The user has not registered any existing farms')
def step_impl(context):
    context.browser.get(context.address + "/register")
    register(context, "IAMANEW", "USER", "joe@nofarms.yet", "pineapple")

@when('the user views the sell page')
def step_impl(context):
    context.browser.get(context.address + "/sell")

@then('the the error: "You dont have any farms yet." is returned')
def step_impl(context):
    assert 'You dont have any farms yet.' in context.browser.page_source

def add_farm(context, name, address1, address2, city, state, country, postcode):
    
    context.browser.find_element_by_name('name').send_keys(name)
    context.browser.find_element_by_name('address1').send_keys(address1)
    context.browser.find_element_by_name('address2').send_keys(address2)
    context.browser.find_element_by_name('city').send_keys(city)
    context.browser.find_element_by_name('state').send_keys(state)
    context.browser.find_element_by_name('country').send_keys(country)
    context.browser.find_element_by_name('postcode').send_keys(postcode)
    context.browser.find_element_by_id("form").submit()   
     
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
    
@given('at the activity page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'farmer_j01@gmail.com', 'louise1993')
    context.browser.get(context.address + "/activity")
    assert 'RECORD ACTIVITY' in context.browser.page_source

@when('a farmer selects their farm, resource and enters a description and date')
def step_impl(context):
    #farm_id = ....
    #resource_id = ..
    record_activity("Plant some seeds",farm_id,timestamp,resource_id)


@then('the activity is reistered for that farm')
def step_impl(context):
    assert 'added new activity' in context.browser.page_source

def record_activity(description,farm_id,date,resource):
    c=context.browser
    c.find_element_by_id("farm_id").send_keys(farm_id)
    c.find_element_by_id("description").send_keys(description)
    c.find_element_by_id("date").send_keys(date)
    c.find_element_by_id("resource").send_keys(resource)
    c.find_element_by_id("form").submit()
