Feature: As a System Owner, I want users to be able to register so that the system can capture necessary to identify
  and verify individual user

  Scenario: Basic registration
    Given I am at the registration page
    When I register as "Frodo", "Baggins", "fbaggins@lotr.com", "frodobaggins" & "frodobaggins"
    Then I receive a success message - "Hello Frodo"

  Scenario: Existing registration
    Given I am at the registration page
    When I register as "Bilbo", "Baggins", "bbaggins@lotr.com", "bilbobaggins" & "bilbobaggins"
    Then I receive the error "Email Id already exists"

  Scenario: Password not equal registration
    Given I am at the registration page
    When I register as "Bruce", "Wayne", "bwayne@wayne.com", "brucewayne" & "brucewayn"
    Then I receive the error "Password mismatch!"

  Scenario: Register with empty form submission
    Given I am at the registration page
    When I register as " ", " ", " ", " " & " "
    Then I receive the error "First Name cannot be empty"
    And I receive the error "Last Name cannot be empty"
    And I receive the error "Email Id cannot be empty"
    And I receive the error "Password cannot be empty"
