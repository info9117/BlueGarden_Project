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
    addcrop(context,"3",  "corn", "plant", "1")
    assert context.browser.page_source

@then('the system should return "You success added crop"')
def step_impl(context):
    assert 'You success added crop' in context.browser.page_source



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
    '''context.browser.find_element_by_name('id').send_keys(id)
    context.browser.find_element_by_name('cropname').send_keys(cropname)
    context.browser.find_element_by_name('growstate').send_keys(growstate)
    context.browser.find_element_by_name('farmid').send_keys(farmid)
    context.browser.find_element_by_name(id).submit()'''
    #context.response = context.browser.page_source



def login(context, email, password):
    email_field = context.browser.find_element_by_id("email")
    password_field = context.browser.find_element_by_id("password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    email_field.submit()




