from behave import *
from features.steps import login, add_produce
import time


@given('I login with "{email}" and "{password}"')
def step_impl(context, email, password):
    context.browser.get(context.address + "/login")
    login(context, email, password)
    assert context.browser.page_source


@given('I visit farm "{farm_id}"')
def step_impl(context, farm_id):
    context.browser.get(context.address + "/farm/" + farm_id + "/produce/add")
    assert context.browser.page_source


@when('I submit produce details "{name}", "{description}", "{category}", "{unit}", "{price}", "{prod_image}"')
def step_impl(context, name, description, category, unit, price, prod_image):
    add_produce(context, name.strip(), description.strip(), category.strip(),
                unit.strip(), price.strip(), prod_image.strip())
    assert context.browser.page_source


@when('I visit the browse produce page')
def step_impl(context):
    context.browser.get(context.address + "/search/produce")
    assert 'Browse Produce' in context.browser.page_source


@then('I see "{name}" in the browse produce page')
def step_impl(context, name):
    assert name in context.browser.page_source


@step('I apply filters location-"{location}", category-"{category}" and search-"{search}"')
def step_impl(context, location, category, search):
    context.browser.get(context.address + "/search/produce?search="+search+"&location="+location+"&"+category+"=on")
    assert context.browser.page_source