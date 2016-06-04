# Created by cruxy at 2016/5/30
Feature: crop process
  As a farmer
  I want to assgin process to  crop
  So that I can know what I need to do in different stage

  # Enter feature description here
  @fast
  Scenario: Farmer choose a process of crop
  Given at the crop screen
  When a farmer choose an crop
  Then a new page display all the activities of that process

  Scenario: Farmer update the process
    Given at the update_Process page
    When a farmer choose a finished activity
    Then this activity will be specified finished