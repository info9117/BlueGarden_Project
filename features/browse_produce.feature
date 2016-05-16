Feature: Browse Produce
  As a user I would like to browse for produce with ability to filter results based on category and location

  Scenario: Browse produce without any filters
    Given I am at home page
    When I go to browse produce page
    Then I see produce in the page
