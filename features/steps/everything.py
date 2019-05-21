from behave import *
from pymodoro import Timer
import time

# *** Setting a timer object ***

@given(u'certain timer parametres')
def step_impl(context):
  def my_callback():
    return 43
  context.callback = my_callback
  context.secs_to_wait = 2
  context.start_time = time.time()

@when(u'I set a timer')
def step_impl(context):
  context.timer = Timer(context.callback, context.secs_to_wait)

@then(u'a callback is called')
def step_impl(context):
  assert context.timer.result is context.callback() 

@then(u'elapsed time is slightly over the timer time')
def step_impl(context):
  context.elapsed = time.time() - context.start_time
  assert context.elapsed > context.secs_to_wait
  assert context.elapsed < context.secs_to_wait + 1


# *** Explicitly telling Pymodoro what I'm working on ***

@given("a certain activity name")
def step_impl(context):
  assert False

@when("I tell Pymodoro that I'm working on it")
def step_impl(context):
  assert False

@then("a 'pymodoro timer' process is launched")
def step_impl(context):
  assert False

@then("the command line is not blocked")
def step_impl(context):
  assert False


# *** Telling Pymodoro I'm working on something, whithout saying what ***

@given("nothing")
def step_impl(context):
  assert False

@when("I tell Pymodoro that I'm working on something")
def step_impl(context):
  assert False


# *** Telling I'm working on something when I'm already working on something ***

@given("I've told Pymodoro I'm working on something")
def step_impl(context):
  assert False

@when("I immediatly say again I'm working on something else")
def step_impl(context):
  assert False

@then("the process fails, I get an exception telling me a pomodoro is already started")
def step_impl(context):
  assert False
