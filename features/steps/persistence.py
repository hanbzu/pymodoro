from behave import *
from pymodoro import dummy

@given("I save a task")
def step_impl(context):
  assert True is not False

@then("I'm able to recover that task")
def step_impl(context):
  assert False
