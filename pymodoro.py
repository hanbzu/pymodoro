#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
from gi.repository import Notify
import sys, time, csv, os, subprocess


# Data files
dataroot = expanduser("~") + "/.config/pymodoro/"

class Processes:
  kill_cmd = "ps -ef | grep $USER | grep 'pymodoro timer' | grep -v grep | awk '{print $2}' | xargs kill"
  get_pid_cmd = "ps -ef | grep $USER | grep 'pymodoro timer' | grep -v grep | awk '{print $2}'"
  @staticmethod
  def kill():
    os.system(Processes.kill_cmd)
  @staticmethod
  def get_pid():
    p = subprocess.Popen(Processes.get_pid_cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = p.communicate()
    return out
  @staticmethod
  def any():
    return Processes.get_pid() != ""

class Persistence:
  @staticmethod
  def save(what, begins, ends):
    with open(dataroot + "history.csv", "a+") as history_file:
      out = csv.writer(history_file, delimiter = ',', quoting = csv.QUOTE_ALL)
      out.writerow((what, Persistence.time_readable(begins), Persistence.time_readable(ends)))
  @staticmethod
  def save_fail(when):
    with open(dataroot + "fail.csv", "a+") as fail_file:
      fail_file.write(Persistence.time_readable(when) + '\n')
  @staticmethod
  def time_readable(a_time): # ISO 8601 format, YYYY-MM-DD for date formatting
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

def timer(what, secs = 25 * 60):
  def callback():
    UX.ring_bell()
    UX.show_notification(what)
  begins = time.gmtime()
  Timer(callback, 5)
  Persistence.save(what, begins, time.gmtime())

def on(what = "Unknown"):
  while Processes.any():
    fail
  os.system("pymodoro timer \"" + what + "\"&")
  print("It's up to you now for the next X mins...")

def fail():
  Processes.kill()
  Persistence.save_fail(time.gmtime())
  print("Auch!")

def reflect():
  print("Reflect: Not implemented")

def error():
  print("Error")

if __name__ == "__main__":
  if (sys.argv[1] == "on"):
    on(sys.argv[2]) if len(sys.argv) else on()
  elif (sys.argv[1] == "timer"):
    timer(sys.argv[2])
  elif (sys.argv[1] == "fail"):
    fail()
  else:
    error()