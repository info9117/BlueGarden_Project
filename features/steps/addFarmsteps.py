import behave
import re

@given('at the sell page')
def step_impl(context):
    context.browser.get(context.address + "/sell")
    MyFarms_found = re.search("My Farms", context.browser.page_source)
    assert MyFarms_found


@when('a farmer submits valid farm <name> and <address>')
def step_impl(context):
    #first login?
    name = "Marrickville Community Garden"
    add_farm(context, "Marrickville Community Garden", "1 Marry St", "", "Marickville", "NSW", "Australia", "2009")
    rv = context.client.get('/sell')
    assert b'Marrickville Community Garden' in rv.data


@then('the the new farm name: <name> is displayed in the My Farms list')
def step_impl(context):
    context.browser.get(context.address + "/sell")
    assert 'Marrickville Community Garden' in context.browser.page_source
    
    
def add_farm(context, name, address1, address2, city, state, country, postcode):
    
    context.browser.find_element_by_name('name').send_keys(name)
    context.browser.find_element_by_name('address1').send_keys(address1)
    context.browser.find_element_by_name('address2').send_keys(address2)
    context.browser.find_element_by_name('city').send_keys(city)
    context.browser.find_element_by_name('state').send_keys(state)
    context.browser.find_element_by_name('country').send_keys(country)
    context.browser.find_element_by_name('postcode').send_keys(postcode)
    context.browser.find_element_by_id("form").submit()
     
