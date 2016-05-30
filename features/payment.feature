Feature: As a System Owner, I want users to be able to pay for the items in their shopping cart by credit card

	Scenario: Basic registration
		Given I am in purchase page
		When I click the payment button
		Then I can enter my credit card details to pay
