Feature: Farmers can register a new active process selected from the process templates, 
            view a list of their active processes, 
            update the progress of a process.
    
    
    @slow
    Scenario: Start a new active process
    Given at the Active_Process page
    When a process, start date, target type and target are selected
    Then the process new active process is initialised and steps populated from the process template
    
