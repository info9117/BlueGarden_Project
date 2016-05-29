Feature: As a System Owner, I want users to be able to register so that the system can capture necessary to identify
	and verify individual user

	Scenario: Basic registration
		Given I am in registration page
		When I register with First name, Last name, Email Id , Password & ConfirmPassword
		Then I should be redirected to "My Dashboard"

	Scenario: Existing registration
		Given I am in registration page
		When I register with First name, Last name, existing Email Id , Password & ConfirmPassword
		Then I should be shown error

	Scenario: Password not equal registration
	    Given I am in registration page
	    When I register with First name, Last name, Email Id , Password & ConfirmPassword(Password and ConfirmPassword is not equal)
	    Then I should be shown the error
