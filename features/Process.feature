Feature: Farmer can create a new process
    As a farmer
    I want to add new processes
    So that I can record activities

    Scenario: Add a new process
    Given at the process page
    When a farmer creates a new process
    Then the new process is recorded

    Scenario: Link from process to activity
    Given at the process page
    When I select an exting process
    Then I  will be directed to the Activity page and the process will be selected

    Scenario: Add a new activity to a process
    Given at the activity page for sathwick user
    When I select an exting process and add an activity
    Then I will be shown the activity added to the process

    Scenario: Cannot add an blank process
    Given at the process page
    When a farmer creates a new process with no name
    Then I will be shown an error message

    Scenario: Cannot add an blank process description
    Given at the process page
    When a farmer creates a new process with no description
    Then I will be shown an error message
