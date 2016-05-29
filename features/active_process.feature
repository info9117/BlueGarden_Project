Feature: Farmers can register a new active process selected from the process templates, 
            view a list of their active processes, 
            update the progress of a process.
    
    

    Scenario: Start a new active process
    Given at the Active_Process page
    When a process, start date, target type and target are selected
    Then the process new active process is initialised and steps populated from the process template
    
    Scenario: Add activities to process template
      Given user arrives at the activity page for a given process template
      When activities are submitted
      Then the activities are stored in sequencial order in the template


    Scenario: Create an actvity
      Given farmer is at the activity page
      When activity description resource and process are entered
      Then the activity is recorded
    @slow
    Scenario: Activity page errors
      Given user is at the activity page
      When the description, resource, or process are not entered
      Then an error is displayed

    Scenario: Process page redirects
      Given farmer is at the process page
      When they click the add procedure or begin process links
      Then the add activity page or active process page appears respectively

    Scenario: active process page errors
      Given farmer is at the active process page
      When they submit without a process or start date specified
      Then the error is displayed