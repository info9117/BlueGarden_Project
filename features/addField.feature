Feature: Farmer user can add a field to their farm
    As a farmer
    I want to identify different areas of the farm
    So that I can track what activities have been applied to different areas of the farm

    Scenario: Add field to existing farm
    Given at the field page
    When a farmer submits new field name and valid farm name
    Then the new field name is recorded with the parent farm


