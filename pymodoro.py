#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
import sys, time, csv, os

# ISO 8601 format that uses YYYY-MM-DD for date formatting

# Data files
dataroot = expanduser("~") + "/.config/pymodoro/"


class Activity:
  def __init__(self, what="Unknown", begins=None, ends=None):
    self.what, self.begins, self.ends = what, begins, ends
  def __repr__(self):
    return self.what + " / " + str(self.begins) + " / " + str(self.ends)
  def saveToDisk(self, where = dataroot + "now.csv"):
    with open(where, "w+") as nowFile:
      out = csv.writer(nowFile, delimiter = ',', quoting = csv.QUOTE_ALL)
      out.writerow((self.what, time.strftime('%Y-%m-%d %H:%M:%S', self.begins), time.strftime('%Y-%m-%d %H:%M:%S', self.ends)))
  @classmethod
  def loadFromDisk(cls):
    return cls("Me")


class Timer:
  def __init__(self, callback, secs, noise = None):
    self.callback, self.secs, self.noise = callback, secs, noise
    self.busy_wait()
  def busy_wait(self):
    time.sleep(self.secs)
    self.result = self.callback()

class Persistence:
  @staticmethod
  def save(what, begins, ends):
    with open(dataroot + "history.csv", "a+") as history_file:
      out = csv.writer(history_file, delimiter = ',', quoting = csv.QUOTE_ALL)
      out.writerow((what, Persistence.time_readable(begins), Persistence.time_readable(ends)))
  @staticmethod
  def time_readable(a_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', a_time)
  @staticmethod
  def interpret_time(a_text):
    return time.strptime(a_text, '%Y-%m-%d %H:%M:%S')

def timer(what = "Unknown", secs = 25 * 60):
  begins = time.gmtime()
  Timer(playSoundBackground, 1)
  Persistence.save(what, begins, time.gmtime())


def writeDateTime(a_time):
  return time.strftime('%Y-%m-%d %H:%M:%S', a_time)

def readDateTime(a_text):
  return time.strptime(a_text, '%Y-%m-%d %H:%M:%S')

def rememberTask(text):
  with open(dataroot + "now.csv", "w+") as nowFile:
    out = csv.writer(nowFile, delimiter = ',', quoting = csv.QUOTE_ALL)
    out.writerow((writeDateTime(time.gmtime()), text))

def getCurrent():
  task = ""
  time_from = 0
  with open(dataroot + "now.csv", "r+") as nowfile:
    for row in csv.reader(nowfile):
      time_from, task = readDateTime(row[0]), row[1]
  open(dataroot + "now.csv", 'w').close() # File is now empty
  return time_from, task

def saveLog(task, a_file):
  with open(a_file, "a+") as tasksFile:
    out = csv.writer(tasksFile, delimiter = ',', quoting = csv.QUOTE_ALL)
    out.writerow((writeDateTime(task['from']), writeDateTime(task['to']), task['what']))

def setAlarm(alarm_code, minutes):
  os.system("echo \"pymodoro alarm " + str(alarm_code) + "\" | at now + " + str(minutes) + " min 2> nul")

def playSoundBackground():
  os.system("aplay ~/hibai/bell.wav&")

def do(text):
  rememberTask(text)
  setAlarm(0, 1)

def fail():
  task = {}
  task['from'], task['what'] = getCurrent()
  task['to'] = time.gmtime()
  print("Auch! Failed while: " + task['what'])
  saveLog(task, dataroot + "fail.csv")

def alarm(what):
  playSoundBackground()
  task = {}
  task['from'], task['what'] = getCurrent()
  task['to'] = time.gmtime()
  if (task['what'] == what):
    playSoundBackground()
    saveLog(task, dataroot + "tasks.csv")

def reflect():
  print("Reflect: Not implemented")

def error():
  print("Error")

def main():
  if (sys.argv[1] == "do"):
    do(sys.argv[2])
  elif (sys.argv[1] == "fail"):
    fail()
  elif (sys.argv[1] == "alarm"):
    alarm()
  elif (sys.argv[1] == "timer"):
    timer()

if __name__ == "__main__":
  main()