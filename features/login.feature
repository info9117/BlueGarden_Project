Feature: As a System Owner, i want users to be able to login so that the system can identify individual users and
  that the system can personalize its services for each user.

  Scenario: Login with existing email and password
    Given I am at the login page
    When I login with "singarisathwik007@gmail.com" and "dm08b048"
    Then I receive a success message - "Hello Sathwik"

  Scenario: Login with invalid email and password
    Given I am at the login page
    When I login with "singarisathwik007@gmail.com" and "dm08b0"
    Then I receive the error "Email Id/Password do not match"

  Scenario: Login with non-registered email and password
    Given I am at the login page
    When I login with "bwayne@wayne.com" and "brucewayne"
    Then I receive the error "User doesn't exist"

  Scenario: Login with empty form
    Given I am at the login page
    When I login with " " and " "
    Then I receive the error "Email Id cannot be empty"
    And I receive the error "Password cannot be empty"