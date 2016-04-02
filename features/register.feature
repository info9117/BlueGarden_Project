Feature: As a System Owner, I want users to be able to register so that the system can capture necessary to identify and verify individual user

	Scenario: Basic registration
		Given I am not currently registered
		When I register with First name, Last name, Email Id & Password
		Then I should be redirected to "My Dashboard"