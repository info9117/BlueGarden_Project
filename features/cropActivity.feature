Feature: farmer users could change their crop to produce
    As a farmer user
    I want to change the grow state of crops 
    so that farmers can change the crop to produce
    
  
    @slow
    Scenario: Change the state of crop to harvested
    Given at the change state screen
    When a famer choose a crop
    Then he could change the state of that crop harvested
    
    Scenario: Change the crop to produce
    Given at the crop screen
    When the state of a crop is harvested
    Then this crop will be changed to produce
    
        
    
    