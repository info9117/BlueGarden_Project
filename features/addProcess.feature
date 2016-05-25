addProcess.feature
Feature: Farmer can create a new process
    As a farmer
    I want to add new processes
    So that I can record activities

    Scenario: Add a new process
    Given at the process page
    When a farmer creates a new process
    Then the new process is recorded
