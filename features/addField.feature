Feature: Farmer user can add a field to their farm
    As a farmer
    I want to identify different areas of the farm
    So that I can track what activities have been applied to different areas of the farm

    Scenario: Add field to existing farm
    Given at the field page
    When a farmer submits new field name and valid farm name
    Then the new field name is recorded with the parent farm

    Scenario: Cannot add field to someone elses farm
    Given at the field page
    When a farmer submits new field name for another farmers farm
    Then I will be advised it is not my farm

    Scenario: Cannot add field to nonexistant farm
    Given at the field page
    When a farmer submits new field name for nonexistant farm
    Then I will be advised it is not my farm

    Scenario: Must add a field name
    Given at the field page
    When I submit without a field name
    Then I will be advised to enter a field name

    Scenario: Must add a farm name
    Given at the field page
    When I submit without a farm name
    Then I will be advised to enter a farm name
