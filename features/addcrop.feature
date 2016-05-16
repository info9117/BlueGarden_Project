Feature: track the state of the crops
    As thg system administor
    I want farmers to be able to track state of crops
    so that farmers can know the state of the crops
    
    Scenario: Add crop to farms
    Given at the crop screen
    When a farmer submit the id cropname, growstate and farm_id
    Then the system should return "You success added crop"
   
       
        
    
    