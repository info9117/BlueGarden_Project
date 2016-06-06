
from behave import *
import re


#add crop
@given('at the crop screen')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    context.browser.get(context.address + "/addcrop")

    #addcrop_found = re.search("add crop", context.browser.page_source)
    assert 'add crop' in context.browser.page_source

@when('a farmer submit the id cropname, growstate and farm_id')
def step_impl(context):
    addcrop(context,"1",  "corn", "plant", "1")
    assert context.browser.page_source

@then('the system should return "You success added crop"')
def step_impl(context):
    assert 'You success added crop' in context.browser.page_source

#change state    
@given('at the change state screen')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')

    context.browser.get(context.address + "/change_state/1")
    assert "change_state" in context.browser.page_source

@when('a famer choose a crop')
def step_impl(context):
    change_state(context, "need some water")
    assert context.browser.page_source

@then ('he could change the state of that crop harvested')
def step_impl(context):
    assert 'you successfully change the state' in context.browser.page_source

@given('at the added crop screen')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    assert context.browser.page_source

@when('the state of a crop is harvested')
def step_impl(context):
    context.browser.get(context.address + "/change_state/1")
    change_state(context, "harvest")
    assert context.browser.page_source

@then('this crop can be changed to produce')
def step_impl(context):
    context.browser.get(context.address + '/farm/1/produce/add')

    assert context.browser.page_source

@when('a farmer choose an crop')
def step_impl(context):
    context.browser.get(context.address + "/update_active_process/113")
    assert context.browser.page_source


@then('a new page display all the activities of that process')
def step_impl(context):
    assert context.browser.page_source

'''@given('at the update_Process page')
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'singarisathwik007@gmail.com', 'dm08b048')
    context.browser.get(context.address + "/update_active_process/113")
    assert  context.browser.page_source

@when('a farmer choose a finished activity')
def step_impl(context):
    set_finish_process(context)
    assert context.browser.page_source

@then('this activity will be specified finished')
def step_impl(context):
    assert 'you successfully finish this acitivity' in context.browser.page_source
    


def set_finish_process(context):
    actid_field = context.browser.find_element_by_id("finishactivity")
    #actid_field.send_keys(set_finish_process)
    actid_field.submit()'''
    

def change_state(context, growstate):
    newGrowState_field = context.browser.find_element_by_id("change_state")
    newGrowState_field.send_keys(growstate)
    newGrowState_field.submit()
    context.response = context.browser.page_source




def addcrop(context, id, cropname, growstate, farmid):
    id_field = context.browser.find_element_by_id("id")
    cropname_field = context.browser.find_element_by_id("cropname")
    growstate_field = context.browser.find_element_by_id("growstate")
    farmid_field = context.browser.find_element_by_id("farmid")
    id_field.send_keys(id)
    cropname_field.send_keys(cropname)
    growstate_field.send_keys(growstate)
    farmid_field.send_keys(farmid)
    id_field.submit()


    #context.response = context.browser.page_source

    
    


def login(context, email, password):
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()



