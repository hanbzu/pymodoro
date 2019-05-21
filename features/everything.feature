Feature: All the features of Pymodoro

  Scenario: Setting a timer object
    Given certain timer parametres
     When I set a timer
     Then a callback is called
      And elapsed time is slightly over the timer time

  Scenario: Explicitly telling Pymodoro what I'm working on
    Given a certain activity name
     When I tell Pymodoro that I'm working on it
     Then a 'pymodoro timer' process is launched
      And the command line is not blocked

  Scenario: Telling Pymodoro I'm working on something, whithout saying what
    Given nothing
     When I tell Pymodoro that I'm working on something
     Then a 'pymodoro timer' process is launched
      And the command line is not blocked

  Scenario: Telling I'm working on something when I'm already working on something
    Given I've told Pymodoro I'm working on something
     When I immediatly say again I'm working on something else
     Then the process fails, I get an exception telling me a pomodoro is already started
  