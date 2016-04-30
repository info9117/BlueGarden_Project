Feature: Farmer user can add a farm which they work on
    As a farmer
    I want to register farms which I work on
    so that I can track the crops and produce related to that farm
    
    Scenario Outline: Add farm to "My Farms" list
    Given at the sell page
    When a farmer submits valid farm <name> and <address>
    Then the the new farm name: <name> is displayed in the My Farms list
    Examples:
        |name|
        |Marrickville Community Garden|
        |Ultimo Rooftop Garden|
        |Parramatta Bee Keepers Cooperative|

    Scenario Outline: Farmer adds existing farm -->Fail
    Given at the sell page
    When a farmer submits an invalid (already existing) farm <name> and <address>
    Then the the error: "Already Exists" is returned
    Examples:
        |name|
        |High St Gardening society|

    
    Scenario Outline: User is not a farmer (yet to add a farm they work on)
    Given The user has not registered any existing farms
    When the user views the sell page
    Then the the error: "You dont have any farms yet." is returned

