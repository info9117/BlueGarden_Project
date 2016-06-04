Feature: As a system owner I want the user can add items into the cart and select the quantity of each item also the
         system should show the total cost.
  
  Scenario Outline: add to cart feature
  Given  the product details page and produce price
  When the user selects the <amount> of the product
    Examples:
     | amount | total |
	 |   1    |2.2    |
	 |   5    |11.0   |
	 |   20   |44.0   |
  Then the system shows the total is <total>
