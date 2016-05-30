# Created by hakur at 15/05/2016
Feature: As a system administrator, I want anyone can contact the firm using this contact form,
  so that the system can notify us when new enquiry is available
  and related apartment can respond properly.

  Scenario Outline: User Submit Contact Form Without Title
    Given user is in contact form page
    When user fills the form with <name>, <email>, <enquiry>, but without <title>
    Then system should show an error to ask user fill title
    Examples:
     | name   | email                | title         | enquiry                          |
	 | Fate   | fate@takamachi.com   |               | I am unhappy -_-##               |
     | Honoka | honoka@takamachi.com |               | I hope this could be improved.   |
     | Nico   | nico@takamachi.com   |               | Why this thing does not work?    |

  Scenario Outline: User Submit Contact Form Without Body
     Given user is in contact form page
     When user fills the form with <name>, <email>, <title>, but without <enquiry>
     Then system should show an error to ask user fill body
     Examples:
     | name   | email                | title         | enquiry                          |
	 | Fate   | fate@takamachi.com   | Hey.          |                                  |
     | Honoka | honoka@takamachi.com | Hmm.          |                                  |
     | Nico   | nico@takamachi.com   | Nico?         |                                  |

  Scenario Outline: User Submit Contact Form Without Email Address
     Given user is in contact form page
     When user fills the form with <name>, <title>, <enquiry>, but without <email>
     Then system should show an error to ask user fill email
     Examples:
     | name   | email                | title         | enquiry                          |
	 | Fate   |                      | Hey.          | I am unhappy -_-##               |
     | Honoka |                      | Hmm.          | I hope this could be improved.   |
     | Nico   |                      | Nico?         | Why this thing does not work?    |


  # needs to amend contact feature file so that it can be a behave test, not unit test.
