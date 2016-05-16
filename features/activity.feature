Feature: Farmer user can add activities to their farm calendar
    As a farmer
    I want to identify different activities on the farm
    So that I can track and record farm activities that have occurred on my farm
    
    Scenario: Record an activity
    Given at the activity page
    When a farmer selects their farm, resource and enters a description and date
    Then the activity is reistered for that farm

    
