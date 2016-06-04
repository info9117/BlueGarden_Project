Feature: As a System Owner, I want farmers to be able to add produce to their farm so that the system can provide them to potential buyers

  Scenario: Add produce details as farm owner
    Given I login with "singarisathwik007@gmail.com" and "dm08b048"
    And I visit farm "1"
    When I submit produce details "Banana", "Big Bananas", "Fruit", "1", "4.38", "/banana.jpg"
    Then I receive a success message - "You successfully added Banana"

  Scenario: Add produce details as farm owner - Empty form
    Given I login with "singarisathwik007@gmail.com" and "dm08b048"
    And I visit farm "1"
    When I submit produce details " ", " ", " ", " ", " ", " "
    Then I receive the error "Name cannot be empty"
    And I receive the error "Description cannot be empty"
    And I receive the error "Please choose a category for the produce"
    And I receive the error "Please choose the units you wish to sell in"
    And I receive the error "Please upload 'png', 'jpg', 'jpeg' or 'gif' image for produce"

  Scenario: Add produce details as farm owner - empty price
    Given I login with "singarisathwik007@gmail.com" and "dm08b048"
    And I visit farm "1"
    When I submit produce details "Banana", "Big Bananas", "Fruit", "1", " ", "/banana.jpg"
    Then I receive the error "Please enter the prices for the produce"

  Scenario: Go To Produce details page - Not farm owner
    Given I login with "bbaggins@lotr.com" and "bilbobaggins"
    And I visit farm "1"
    Then I receive the error "Sorry, This farm doesn't belong to you"