from behave import *
import re


#add crop    
@given('at the crop screen')  
def step_impl(context):
    context.browser.get(context.address + "/crop")
    addcrop_found = re.search("add_crop", context.browser.page_source)
    assert addcrop_found
    
@when('a farmer submit the <cropname>, <growstate> and <farmid>')
def step_impl(context,cropname,growstate, farmid):
    addcrop(context, cropname, growstate, farmid)
    
    



def addcrop_backup(context, id, crop_name, grow_state, farm_id):
    id_field = context.browser.find_element_by_id("id")
    cropname_field = context.browser.find_element_by_id("crop_name")
    growstate_field = context.browser.find_element_by_id("grow_state")
    farmid_field = context.browser.find_element_by_id("farm_id")
    id_field.send_keys(id)
    cropname_field.send_keys(crop_name)
    growstate_field.send_keys(grow_state)
    farmid_field.send_keys(farm_id)
    
def addcrop(context, crop_name, grow_state, farm_id):
    #id_field = context.browser.find_element_by_id("id")
    cropname_field = context.browser.find_element_by_id("crop_name")
    growstate_field = context.browser.find_element_by_id("grow_state")
    farmid_field = context.browser.find_element_by_id("farm_id")
    #id_field.send_keys(id)
    cropname_field.send_keys(crop_name)
    growstate_field.send_keys(grow_state)
    farmid_field.send_keys(farm_id)  
    context.response = context.browser.page_source

    
@then('the system should return "{text}"')
def step_impl(context,text):
    assert text in context.response