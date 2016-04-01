Feature: As a System Owner, I want users to be able to register so that the system can capture necessary to identify and verify individual user

	Scenario: Basic registration
		Given I am an user
			And I am not currently registerd
		When I go to the "Register Screen"
			And I fill in "First Name (required)"
			And I fill in "Last Name (required)"
			And I fill in "Email Id (required)"
			And I fill in "Password (required)"
			And I fill in "Password Confirmation"
			And I click "Register"
		Then I should be redirected to "My Dashboard"