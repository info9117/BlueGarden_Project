Feature: track the state of the crops
    As thg system administor
    I want farmers to be able to track state of crops
    so that farmers can know the state of the crops
    
    Scenario Outline: Add crop to farms
    Given at the crop screen
    When a farmer submit the <cropname>
    Then the system should return "successfully added"
    Examples:
        |cropname|
        |corn|
        |banana|
        |wheat|
        |redbull|
        
        
    Scenario Outline: remove crop from farms
    Given at the crop screen
    When a farmer submit the <cropname>
    Then the system should return "successfully removed"
    Examples:
        |cropname|
        |corn|
        |banana|
        |wheat|
        |redbull|
        
    Scenario Outline: add crop to not empty farm
    Given at the crop screen
    When a farmer submit the <cropname>
    Then the system should return "sorry, this farm has no place for more crops"
    Examples:
        |cropname|
        |corn|
        |banana|
        |wheat|
        |redbull|
        
    Scenario Outline: show the state of crops
    Given at the crop screen
    When a farmer choose one farm
    Then the system should return growing states of all 
    