# Created by hakur at 16/05/2016
Feature: As a company manager, I want a portal to access all feedback data
  and I can view the feedback efficiently

  Scenario Outline: View Customer Feedback
    Given I am logged in as a manager
    When I open feedback management portal
    Then system should display all received feedback, including <name>, <email>, <title>, <enquiry>
    Examples:
      | name   | email                | title         | enquiry                          |
	  | Fate   | fate@takamachi.com   | Hey.          | I am unhappy -_-##               |
      | Honoka | honoka@takamachi.com | Hmm.          | I hope this could be improved.   |
      | Nico   | nico@takamachi.com   | Nico?         | Why this thing does not work?    |