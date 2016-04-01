Feature: As a System Owner, i want users to be able to login so that the system can identify individual users and that the system can personalize its services for each user.

	Scenario: Login with existing email and password
		Given I am an "User"
			And I am not currently logged in
		When I go to the "Login Screen"
			And I fill in "Email Id (required)"
			And I fill in "Password (required)"
			And I click "Login"
		Then I will be redirected to "My Dashboard"