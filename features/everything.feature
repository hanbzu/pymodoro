Feature: showing off behave

  Scenario: run a simple test
     Given we have behave installed
      when we implement a test
      then behave will test it for us!

  Scenario: remember a task
    Given I save a task
     then I'm able to recover that task