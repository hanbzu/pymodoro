PyModoro
========

# REFLECTION

Proposals:
* Reflection changes depending on time of the day. Before going to bed: About tomorrow (too much stress?)

Information:
* Notify if there is agenda for today or tomorrow
* Today: What needs to be done (depending on plan)
* Today: Time available (depending on plan)
* Deadlines comming: Almost here (urgent things?)

It's comming
* Most relevant deadlines
* Relevant depends on time left and difficulty


# AGENDA

* Booooh things scheduled for today (those with start and end date)
* Free time today
* Available time for work today
* Available time for work next X days


# DATA

.unetasks
* task, [parent_task], [size], [done]
* a tree structure for organising tasks
* once one une is started task is added if not already there
* size is an estimator and is optional
* done is also optional, done tasks are kept for reference

.unehistory
* from, to, [what]
* from and to are date-times
* Once une times out a line is added
* The line means: what is being done from from to to
* Lines are never removed

.unefails
* from, to, [what]
* from and to are date-times
* This is where interruptions are recorded
* Interruptions can feature what was being done
* Lines are never removed

.uneplan
* [after], [before], what
* what can be a task, or something else
* either after, or before or both
* if there's only after, 43 folders style, a reminder, creator or tasks
* if there's only before, thats a deadline, deadlines are coming
* if there's box, some fixed thing ahead. Maybe a meeting. Boooh.

.unehabits
* from, to, periodicity, what, [similar_thing]
* what is never a task here
* from and to are times, not dates
* periodicity is weekly or monthly
* weekends are sacred, out of the scope
* holidays and free days and sabatic periods are sacred, out of scope
