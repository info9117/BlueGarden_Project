Feature: As a System Owner, I want users to be able to register so that the system can capture necessary to identify
	and verify individual user

	Scenario: Basic registration
		Given I am in registration page
		When I enter my Email
		Then I should be redirected to "My Dashboard"

	Scenario: Existing registration
		Given I am in registration page
		When I register with First name, Last name, existing Email Id & Password
		Then I should be shown an error