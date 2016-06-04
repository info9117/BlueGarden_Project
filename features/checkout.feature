Feature:as a system owner I want the client is able to checkout and saves all the billing information

  Scenario Outline: checkout feature
    Given the user at the checkout page
    When the user enters his <name> <email> <phone> <address> <discount> and clicks on save buyer info
    Examples:
     | name   | email         | phone | address    | discount |
	 |   mike |mike@gmail.com |123456 | Burnett    | 11111    |
	 |   john |john@gmail.com |657788 | merrylands | 22222    |
	 |   ray  |ray@gmail.com  |546789 | redfern    | 33333    |
    Then the system saves the information into the database and shows success message to the user and total value of item and total value after discount