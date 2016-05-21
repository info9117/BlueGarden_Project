Feature: Farmer user can record activities
    As a farmer
    I want to identify different activities on the farm
    So that I can track and record farm activities that have 
    occurred throughout farm processes
    
    Scenario: Record an activity
    Given at the activity page
    When a farmer enters a resource and enters a description
    Then the new activity is recorded
"""    
    Scenario not yet implemented: Record a duplicate activity
    Given at the activity page
    When a farmer enters a resource and enters a description that matches an existing entry
    Then the an error "already exists" is displayed

"""    
