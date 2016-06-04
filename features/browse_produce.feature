Feature: Browse Produce
  As a user I would like to browse for produce with ability to filter results based on category and location

  Scenario: Browse produce without any filters
    When I visit the browse produce page
    Then I see "corn" in the browse produce page

  Scenario: Browse produce with filters
    When I visit the browse produce page
    And I apply filters location-"Sydney", category-"Vegetable" and search-"cor"
    Then I see "corn" in the browse produce page