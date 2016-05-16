# Created by hakur at 16/05/2016
Feature: As a company manager, I want a portal to access all feedback data
  and I can view the feedback efficiently

  Scenario: View Customer Feedback
    Given I am logged in to system
    When I open feedback management portal
    Then system should display all received feedback
