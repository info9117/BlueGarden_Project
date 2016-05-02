Feature: As a System Owner, I want users to be able to reset their password if they forget it

	Scenario: Get to reset
		Given I am in the login page
		When I click reset password
		Then I should be redirected to "password reset"

	Scenario: Reset
		Given I am in password reset page
		When I enter my email
		Then I should recieve an email to that email with reset instructions