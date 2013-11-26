#!/usr/bin/env python
# -*- coding: utf-8 -*-

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

  def disable(self):
    self.HEADER = ''
    self.OKBLUE = ''
    self.OKGREEN = ''
    self.WARNING = ''
    self.FAIL = ''
    self.ENDC = ''

print bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC

#import json
#json.load(open('/tmp/config.json'))   