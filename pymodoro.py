#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
from gi.repository import Notify
from dateutil import tz
import sys, time, datetime, csv, os, subprocess, json

class Conf:
  DATAROOT = expanduser("~") + "/.config/pymodoro/"
  def __init__(self):
    self.history_file = Conf.DATAROOT + 'history.csv'
    self.fail_file = Conf.DATAROOT + 'fail.csv'
    with open(Conf.DATAROOT + 'config.json') as config:
      j = json.load(config)
      self.pomodoro_mins, self.timeout_sound, self.noise = j['pomodoro_mins'], j['timeout_sound'], j['noise']
      self.noise = None if (self.noise == "") else Conf.DATAROOT + self.noise
      self.timeout_sound = None if (self.timeout_sound == "") else Conf.DATAROOT + self.timeout_sound

class Proc:
  def __init__(self):
    pass
  def kill(self, pid):
    if (pid != ''): os.system('kill ' + pid)
  def get_pid(self, target):
    p = subprocess.Popen("ps -ef | grep $USER | grep '" + target + "' | grep -v grep | awk '{print $2}'",
                         shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = p.communicate()
    return out
  def any(self):
    return self.get_pid('pymodoro timer') != ""

class Persistence:
  TXT_TIME_FORMAT = '%Y-%m-%d %H:%M:%S' # ISO 8601 format, YYYY-MM-DD for date formatting
  def __init__(self, conf):
    self.conf = conf
  def save(self, what, begins, ends):
    with open(self.conf.history_file, "a+") as history_file:
      out = csv.writer(history_file, delimiter = ',', quoting = csv.QUOTE_ALL)
      out.writerow((what, self.time_readable(begins), self.time_readable(ends)))
  def load(self):
    slot_list = []
    with open(conf.history_file, 'rb') as historyfile:
      for row in csv.reader(historyfile, delimiter = ',', quoting = csv.QUOTE_ALL):
        (what, begins, ends) = (row[0], self.time_from_text_utc(row[1]), self.time_from_text_utc(row[2]))
        slot_list.append([what, begins, ends])
    return slot_list
  def save_fail(self, when):
    with open(self.conf.fail_file, "a+") as fail_file:
      fail_file.write(self.time_readable(when) + '\n')
  def time_readable(self, a_time): # a_time must be in UTC
    return time.strftime(Persistence.TXT_TIME_FORMAT, a_time)
  def time_from_text_utc(self, a_text_utc_time): # Returned time will be localtime
    return datetime.datetime.strptime(a_text_utc_time, Persistence.TXT_TIME_FORMAT)

class UX:
  DIM_GREEN = '\033[32m'
  ENDC = '\033[0m'
  @staticmethod
  def utc_time_vis(utc_time, format):
    return utc_time.replace(tzinfo = tz.tzutc()).astimezone(tz.tzlocal()).strftime(format)
  @staticmethod
  def show_notification(what):
    Notify.init('Summary-Body')
    Notify.Notification.new('Pomodoro elapsed', 'while working on ' + what, '').show()
  @staticmethod
  def play_audio(audio_file, background = True, secs = None):
    if audio_file:
      if 'wav' in audio_file.lower():
        if background: os.system('aplay ' + audio_file + ' 2> /dev/null&')
        else: os.system('aplay ' + audio_file + ' -d ' + str(secs) + '2> /dev/null&')
      elif 'mp3' in audio_file.lower():
        if background: os.system('mpg123 ' + audio_file + ' > /dev/null&')
        else:
          p = subprocess.Popen(['mpg123', audio_file], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
          time.sleep(secs)
          p.kill()

class Timer:
  def __init__(self, callback, secs, noise = None):
    self.callback, self.secs, self.noise = callback, secs, noise
    self.busy_wait()
  def busy_wait(self):
    if (self.noise):
      UX.play_audio(self.noise, background = False, secs = self.secs)
    else:
      time.sleep(self.secs)
    self.result = self.callback()

class Chart:
  BLOCKS = u'▁▂▃▄▅▆▇██'
  @staticmethod
  def spark(data, line = '', lo = None, hi = None):
    if lo == None:
      lo = float(min(data))
    else:
      data = [lo if (d < lo) else d for d in data]
    if hi == None:
      hi = float(max(data))
    else:
      data = [hi if (d > hi) else d for d in data]
    incr = (hi - lo) / 8
    return ''.join([Chart.BLOCKS[int((float(n) - lo) / incr)] for n in data])   

class Zeitgeist:
  @staticmethod
  def popular_terms(term_list):
    term_counter =  {}
    for term in term_list:
      if term in term_counter: term_counter[term] += 1
      else: term_counter[term] = 1
    return sorted(term_counter, key = term_counter.get, reverse = True)
  @staticmethod
  def most_common(persistence, how_many):
    term_list = [item[0] for item in persistence.load()]
    return Zeitgeist.popular_terms(term_list)[:how_many]
  @staticmethod
  def last_ones(persistence, how_many):
    readable_list = [item[0] + " at " + UX.utc_time_vis(item[1], '%H.%M') for item in persistence.load()]
    return readable_list[-how_many:]
  @staticmethod
  def get_by_day(persistence): # By day list is in local time
    by_day = {}
    for item in persistence.load():
      day = UX.utc_time_vis(item[1], '%Y-%m-%d') # Conversion from UTC in utc_time_vis!
      if day not in by_day:
        by_day[day] = []
      by_day[day].append(item)
    return by_day
  @staticmethod
  def daily_pomodoros(persistence): # In local time
    pomodoros_by_day = {}
    by_day = Zeitgeist.get_by_day(persistence)
    for day in by_day:
      pomodoros_by_day[day] = len(by_day[day])
    return pomodoros_by_day
  @staticmethod
  def punchcard_list(persistence, how_many_days):
    days = [datetime.date.today() - datetime.timedelta(days = d) for d in range(0, how_many_days - 1)]
    reversed_days = days[::-1]
    day_keys = [day.strftime('%Y-%m-%d') for day in reversed_days]
    punchcard = []
    pomodoros = Zeitgeist.daily_pomodoros(persistence)
    for day in day_keys:
      if day in pomodoros: punchcard.append(pomodoros[day])
      else: punchcard.append(0)
    return punchcard

# *** Functionality ***

def timer(conf, persistence, what, secs):
  def callback():
    UX.play_audio(conf.timeout_sound)
    UX.show_notification(what)
  begins = time.gmtime()
  Timer(callback, secs, conf.noise)
  persistence.save(what, begins, time.gmtime())

def on(conf, persistence, proc, what = "Unknown"):
  while proc.any():
    fail(persistence, proc)
  os.system('pymodoro timer \"' + what + '\" ' + str(conf.pomodoro_mins * 60) + ' &')
  end_time = (datetime.datetime.now() + datetime.timedelta(minutes = conf.pomodoro_mins)).strftime('%H.%M')
  print("I'll tap you on the shoulder in " + str(conf.pomodoro_mins) + " mins (" + end_time + ")")

def fail(persistence, proc):
  persistence.save_fail(time.gmtime())
  proc.kill(proc.get_pid('pymodoro timer'))
  proc.kill(proc.get_pid('mpg123')) # Kill noise
  print("Auch!")

def reflect(persistence):
  print(UX.DIM_GREEN + "Most recent history is" + UX.ENDC)
  print('\n'.join(Zeitgeist.last_ones(persistence, 5)))
  print(UX.DIM_GREEN + "Most common terms are" + UX.ENDC)
  print(', '.join(Zeitgeist.most_common(persistence, 3)))
  print(UX.DIM_GREEN + "Punchcard" + UX.ENDC)
  punchcard = Zeitgeist.punchcard_list(persistence, 30)
  print(Chart.spark(punchcard) + " today " + str(punchcard[-1]))
  print("Average is " + str(sum(punchcard) / len(punchcard)) + " with maximum at " + str(max(punchcard)))

if __name__ == "__main__":

  # Toolset
  conf = Conf()
  persistence = Persistence(conf)
  proc = Proc()

  # Routing
  if len(sys.argv) == 1:
    on(conf, persistence, proc)
  elif (sys.argv[1] == "on"):
    on(conf, persistence, proc, sys.argv[2]) if len(sys.argv) == 3 else on(conf, persistence, proc)
  elif (sys.argv[1] == "timer"):
    timer(conf, persistence, sys.argv[2], int(sys.argv[3]))
  elif (sys.argv[1] == "fail"):
    fail(persistence, proc)
  elif (sys.argv[1] == "reflect"):
    reflect(persistence)
  else:
    print("pymodoro on|fail|reflect [task]")