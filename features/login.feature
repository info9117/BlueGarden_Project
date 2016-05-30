Feature: As a System Owner, i want users to be able to login so that the system can identify individual users and
	that the system can personalize its services for each user.

	Scenario: Login with existing email and password
		Given I am in the login page
		When I login with email and password
		Then I will be redirected to "My Dashboard"

	Scenario: Login with invalid email and password
		Given I am in the login page
		When I login with invalid email and password
		Then I will be shown error