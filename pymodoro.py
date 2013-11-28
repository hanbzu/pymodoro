#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
from gi.repository import Notify
import sys, time, csv, os, subprocess, json

class Conf:
  DATAROOT = expanduser("~") + "/.config/pymodoro/"
  def __init__(self):
    self.history_file = Conf.DATAROOT + 'history.csv'
    self.fail_file = Conf.DATAROOT + 'fail.csv'

class Proc:
  CMD_KILL = "ps -ef | grep $USER | grep 'pymodoro timer' | grep -v grep | awk '{print $2}' | xargs kill"
  CMD_GET_PID = "ps -ef | grep $USER | grep 'pymodoro timer' | grep -v grep | awk '{print $2}'"
  def __init__(self):
    pass
  def kill(self):
    os.system(Proc.CMD_KILL)
  def get_pid(self):
    p = subprocess.Popen(Proc.CMD_GET_PID, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = p.communicate()
    return out
  def any(self):
    return self.get_pid() != ""

class Persistence:
  def __init__(self, conf):
    self.conf = conf
  def save(self, what, begins, ends):
    with open(self.conf.history_file, "a+") as history_file:
      out = csv.writer(history_file, delimiter = ',', quoting = csv.QUOTE_ALL)
      out.writerow((what, self.time_readable(begins), self.time_readable(ends)))
  def save_fail(self, when):
    with open(self.conf.fail_file, "a+") as fail_file:
      fail_file.write(self.time_readable(when) + '\n')
  def time_readable(self, a_time): # ISO 8601 format, YYYY-MM-DD for date formatting
    return time.strftime('%Y-%m-%d %H:%M:%S', a_time)

class UX:
  @staticmethod
  def ring_bell():
    os.system("aplay ~/.config/pymodoro/alarm1.wav 2> /dev/null&")
  @staticmethod
  def show_notification(what):
    Notify.init("Summary-Body")
    Notify.Notification.new("Pomodoro elapsed", "while working on " + what, "").show()

class Timer:
  def __init__(self, callback, secs, noise = None):
    self.callback, self.secs, self.noise = callback, secs, noise
    self.busy_wait()
  def busy_wait(self):
    time.sleep(self.secs)
    self.result = self.callback()


# *** Functionality ***

def timer(persistence, what, secs = 25 * 60):
  def callback():
    UX.ring_bell()
    UX.show_notification(what)
  begins = time.gmtime()
  Timer(callback, 5)
  persistence.save(what, begins, time.gmtime())

def on(persistence, proc, what = "Unknown"):
  while proc.any():
    fail(persistence)
  os.system("pymodoro timer \"" + what + "\"&")
  print("It's up to you now for the next X mins...")

def fail(persistence, proc):
  proc.kill()
  persistence.save_fail(time.gmtime())
  print("Auch!")

def reflect(persistence):
  print("Reflect: Not implemented")


if __name__ == "__main__":

  # Toolset
  conf = Conf()
  prst = Persistence(conf)
  proc = Proc()

  # Routing
  if len(sys.argv) == 1:
    on(prst, proc)
  elif (sys.argv[1] == "on"):
    on(prst, proc, sys.argv[2]) if len(sys.argv) == 3 else on(prst, proc)
  elif (sys.argv[1] == "timer"):
    timer(prst, sys.argv[2])
  elif (sys.argv[1] == "fail"):
    fail(prst, proc)
  elif (sys.argv[1] == "reflect"):
    reflect(prst)
  else:
    print("pymodoro on|fail|reflect [task]")