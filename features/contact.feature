# Created by hakur at 15/05/2016
Feature: As a system administrator, I want anyone can contact the firm using this contact form,
  so that the system can notify us when new enquiry is available
  and related apartment can respond properly.

  Scenario: User Submit Contact Form Without Title
    Given user is in contact form page
    When user fills the form without title
    Then system should show an error to ask user fill title

  Scenario: User Submit Contact Form Without Body
     Given user is in contact form page
     When user fills the form without body
     Then system should show an error to ask user fill body

  Scenario: User Submit Contact Form Without Email Address
     Given user is in contact form page
     When user fills the form without email address
     Then system should show a warning


  # needs to amend contact feature file so that it can be a behave test, not unit test.