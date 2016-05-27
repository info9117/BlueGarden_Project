# Created by cruxy at 2016/5/27
Feature: add resource_list
  As a farmer user
  I want I can add resource to the system
  so that workers can know how many resources they can use
  @slow
  Scenario: add a resource to a resourcelist
    Given at the add resource page
    When a user input the resource decription
    Then he can add this resource to the resource list
    # Enter steps here