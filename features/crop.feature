Feature: track the state of the crops
    As thg system administor
    I want farmers to be able to track state of crops
    so that farmers can know the state of the crops
    
    Scenario: Add crop to farms
    Given at the crop screen
    When a farmer submit the id cropname, growstate and farm_id
    Then the system should return "You success added crop"
   
    Scenario: Track the state of crop
    Given at the crop screen
    When a farmer login as a farmer
    Then the system should show all the details of crops
    
    Scenario: Change the state of crop
    Given at the crop screen
    When a famer choose a crop
    Then he could change the state of that crop
    
    Scenario: Change the crop to produce
    Given at the crop screen
    When the state of a crop is harvested
    Then this crop will be changed to produce
    
        
    
    