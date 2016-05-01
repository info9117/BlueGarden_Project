Feature: Farmer user can add a farm which they work on
    As a farmer
    I want to register farms which I work on
    so that I can track the crops and produce related to that farm
    
    Scenario: Add farm to "My Farms" list
    Given at the sell page
    When a farmer submits valid farm name and address
    Then the new farm name is displayed in the My Farms list

    Scenario: Farmer adds existing farm -->Fail
    Given logged in at the sell page
    When a farmer submits an invalid (already existing) farm name
    Then the the error: "Already Exists" is returned
    
    Scenario: User is not a farmer (yet to add a farm they work on)
    Given The user has not registered any existing farms
    When the user views the sell page
    Then the the error: "You dont have any farms yet." is returned
