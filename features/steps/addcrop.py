from behave import *
import re


#add crop    
@given('at the crop screen')  
def step_impl(context):
    context.browser.get(context.address + "/login")
    login(context, 'bbaggins@lotr.com', 'bilbobaggins')
    context.browser.get(context.address + "/addcrop")
    
    addcrop_found = re.search("add crop", context.browser.page_source)
    assert addcrop_found
    
@when('a farmer submit the <id> <cropname>, <growstate> and <farm_id>')
def step_impl(context,id, cropname,growstate, farm_id):
    
    addcrop(context,"1",  "corn", "plant", "1")
    
@then('the system should return "{text}"')
def step_impl(context):
    assert 'You success added crop' in context.context.browser.page_source    



def addcrop(context, id, crop_name, grow_state, farm_id):
    id_field = context.browser.find_element_by_id("id")
    cropname_field = context.browser.find_element_by_id("crop_name")
    growstate_field = context.browser.find_element_by_id("grow_state")
    farmid_field = context.browser.find_element_by_id("farm_id")
    id_field.send_keys(id)
    cropname_field.send_keys(crop_name)
    growstate_field.send_keys(grow_state)
    farmid_field.send_keys(farm_id)
    
    
    
def login(context, email, password):
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()
    

    

    