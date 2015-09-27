#!/usr/bin/python
# 
# Filename: ec2-power.py
# Version: 0.1.0
# Author: Ade
# Description: boto startup/shutdown script based on auto:[start/stop/ignore] cron tags
# 

import boto.ec2
import croniter
import datetime

debug = 1

region = 'ap-southeast-2'
a_term = 'disableApiTermination'
a_stop = 'instanceInitiatedShutdownBehavior'

def time_to_action(sched, now, seconds):
   try:
      cron = croniter.croniter(sched, now)
      d1 = now + datetime.timedelta(0, seconds)
      if (seconds > 0):
         d2 = cron.get_next(datetime.datetime)
         ret = (now < d2 and d2 < d1)
      else:
         d2 = cron.get_prev(datetime.datetime)
         ret = (d1 < d2 and d2 < now)
      print "now: %s / d1: %s / d2: %s" % (now, d1, d2)
   except:
      ret = False
   print "time_to_action: %s" % ret
   return ret

now = datetime.datetime.now()
print "===================================="
print "RUNTIME = %s" % now

conn=boto.ec2.connect_to_region(region)
reservations = conn.get_all_instances()

start_list = []
stop_list = []

for res in reservations:
   for inst in res.instances:
      state = inst.state
      name = inst.tags['Name'] if 'Name' in inst.tags else 'Unknown'
      start_sched = inst.tags['auto:start'] if 'auto:start' in inst.tags else None
      stop_sched = inst.tags['auto:stop'] if 'auto:stop' in inst.tags else None
      term = 1 if conn.get_instance_attribute(inst.id, a_term, dry_run=False)[a_term] else 0
      stop = 1 if conn.get_instance_attribute(inst.id, a_stop, dry_run=False)[a_stop] == 'stop' else 0
      ignore = 1 if 'auto:ignore' in inst.tags else 0
      print "(%s) %-30s [%s] (%s/%s/%s) [%s] [%s]" % (inst.id, name, state, term, stop,
                                                      ignore, start_sched, stop_sched)

      if start_sched != None and state == "stopped" and time_to_action(start_sched, now, 16 * 60):
          start_list.append(inst.id)
      if stop_sched != None and state == "running" and time_to_action(stop_sched, now, 31 * -60):
        if term and stop and ignore == 0:
          stop_list.append(inst.id)
        else:
          print "ignoring stop of %s - term[%s], stop[%s], ignore[%s]" % (inst.id, term, stop, ignore)

print
if len(start_list) > 0:
   if debug:
      print "would start: %s" % start_list
   else:
      ret = conn.start_instances(instance_ids=start_list, dry_run=False)
      print "start_instances %s" % ret
if len(stop_list) > 0:
   if debug:
      print "would stop: %s" % stop_list
   else:
      ret = conn.stop_instances(instance_ids=stop_list, dry_run=False)
      print "stop_instances %s" % ret
