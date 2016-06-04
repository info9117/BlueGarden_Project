from behave import *
from models import *
from main import app
db.app=app
db.init_app(app)
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
    context.browser.get(context.address + "/activity/0")
    assert 'Add Activity to Process' in context.browser.page_source

@when('a farmer enters a resource and enters a description')
def step_impl(context):

    resource = "1"
    process = "1"
    description = "Activity on farm"
    record_activity(context,process, resource,description)

@then('the new activity is recorded')
def step_impl(context):
    assert "Activity \"Activity on farm\" was added to making cheese" in context.browser.page_source

def record_activity(context,process, resource,description):
    c=context.browser
    c.find_element_by_id("description").send_keys(description)
    c.execute_script('$(function() { $("#resource").val("'+resource+'"); });')
    c.execute_script('$(function() { $("#process").val("'+process+'"); });')
    c.find_element_by_id("form").submit()

@given('at the Active_Process page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'farmer_j01@gmail.com', 'louise1993')
    context.browser.get(context.address + "/active_process/process/1")
    assert 'Start a new Process' in context.browser.page_source

@when('a process, start date, target type and target are selected')
def step_impl(context):
    c=context.browser
    target="other"
    c.execute_script('$(function() { $("#target").val("'+target+'"); });')
    c.find_element_by_id("form").submit()
    c.find_element_by_id("other_target").send_keys("On the roof!")
    date="10 Sep, 2016"
    c.execute_script('$(function() { $("#date").val("'+date+'"); });')
    c.find_element_by_id("form").submit()	
	
@then('the process new active process is initialised and steps populated from the process template')
def step_impl(context):
    assert 'New active process' in context.browser.page_source
	
@given('user arrives at the activity page for a given process template')
def step_impl(context):
    c=context.browser
    c.get(context.address + "/login")
    login(context, 'farmer_j01@gmail.com', 'louise1993')
    c.get(context.address + "/activity/1")
    assert 'Add Activity to Process '+"\"making cheese\"" in context.browser.page_source
	
@when('activities are submitted')
def step_impl(context):
    record_activity(context,'1', '1',"First step in process")
    assert "Activity \"First step in process\" was added to making cheese" in context.browser.page_source
    record_activity(context,'1', '1',"Second step in process")
    assert "Activity \"Second step in process\" was added to making cheese" in context.browser.page_source
	
@then('the activities are stored in sequencial order in the template')
def step_ipml(context):
    #assert table order of process steps
    step1 = Process_Steps.query.filter_by(procedure_id=1).first()
    step2 = Process_Steps.query.get(step1.id+1)
    activity1 = Activity_List.query.get(step1.activity_id).activity_description
    activity2 = Activity_List.query.get(step2.activity_id).activity_description
    assert "First step in process" == activity1
    assert "Second step in process" == activity2

@Given('farmer is at the activity page')
def step_impl(context):
    c=context.browser
    c.get(context.address + "/login")
    login(context, 'farmer_j01@gmail.com', 'louise1993')
    c.get(context.address + "/activity/0")
    assert 'Add Activity to Process' in context.browser.page_source
@when('activity description resource and process are entered')
def step_impl(context):
    record_activity(context,'1', '1',"First step in process")
@then('the activity is recorded')
def step_ipml(context):
    assert "Activity \"First step in process\" was added to making cheese" in context.browser.page_source
@Given('user is at the activity page')
def step_impl(context):
    c=context.browser
    c.get(context.address + "/login")
    login(context, 'farmer_j01@gmail.com', 'louise1993')
    c.get(context.address + "/activity/0")
    assert 'Add Activity to Process' in context.browser.page_source
@when('the description, resource, or process are not entered')
def step_impl(context):
    record_activity(context,'1', '',"description")
    assert "select a resource this time" in context.browser.page_source
    record_activity(context,'', '1',"description")
    assert "select a process" in context.browser.page_source
    record_activity(context,'1', '1','')
@then('an error is displayed')
def step_ipml(context):
    assert "add an activity description" in context.browser.page_source

@Given('farmer is at the process page')
def step_impl(context):
    c=context.browser
    c.get(context.address + "/login")
    login(context, 'farmer_j01@gmail.com', 'louise1993')
    c.get(context.address + "/process")
    assert 'Add a new Process' in context.browser.page_source
@when('they click the add procedure or begin process links')
def step_impl(context):
    c=context.browser
    c.find_element_by_id("procedurelink").click()
    assert 'Add Activity to Process' in context.browser.page_source
    c.get(context.address + "/process")
    c.find_element_by_id("processlink").click()
@then('the add activity page or active process page appears respectively')
def step_ipml(context):
    assert 'Start a new Process' in context.browser.page_source

@given('farmer is at the active process page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'farmer_j01@gmail.com', 'louise1993')
    context.browser.get(context.address + "/active_process/process/0")
    assert 'Start a new Process' in context.browser.page_source

@when('they submit without a process or start date specified')
def step_impl(context):
    c=context.browser
    process="1"
    date="10 Sep, 2016"
    c.execute_script('$(function() { $("#date").val("'+date+'"); });')
    c.find_element_by_id("form").submit()
    assert 'A process and start date must be selected' in context.browser.page_source
    c.execute_script('$(function() { $("#process").val("'+process+'"); });')
    c.find_element_by_id("form").submit()
@then('the error is displayed')
def step_impl(context):
    assert 'A process and start date must be selected' in context.browser.page_source
