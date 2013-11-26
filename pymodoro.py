#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
import sys, time, csv, os
from time import gmtime

# ISO 8601 format that uses YYYY-MM-DD for date formatting

# Data files
dataroot = expanduser("~") + "/.config/pymodoro/"

def dummy(x, y):
  return x + y

def writeDateTime(a_time):
  return time.strftime('%Y-%m-%d %H:%M:%S', a_time)

def readDateTime(a_text):
  return time.strptime(a_text, '%Y-%m-%d %H:%M:%S')

def rememberTask(text):
  with open(dataroot + "now.csv", "w+") as nowFile:
    out = csv.writer(nowFile, delimiter = ',', quoting = csv.QUOTE_ALL)
    out.writerow((writeDateTime(gmtime()), text))

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
  task['to'] = gmtime()
  print("Auch! Failed while: " + task['what'])
  saveLog(task, dataroot + "fail.csv")

def alarm(what):
  playSoundBackground()
  task = {}
  task['from'], task['what'] = getCurrent()
  task['to'] = gmtime()
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
  elif (sys.argv[1] == "reflect"):
    reflect()

if __name__ == "__main__":
  main()