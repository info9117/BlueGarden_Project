Feature: As a System Owner, I want users to be able to reset their password if they forget it

	Scenario: Reset password
		Given I am in reset password page
		When I enter my email
		Then I will be redirected to "resetdone"

	Scenario: Reset wrong
		Given I am in reset password page
		When I enter an unregistered email
		Then Email not registered error is shown