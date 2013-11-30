PyModoro
========

Pymodoro is a highly opinionated script that helps you break down your work into small 25 minute bits or [pomodoros](http://pomodorotechnique.com/) and record your time usage automatically. This way you can focus on your task while you are doing it and leave Pymodoro do the logging and visualising work.

### Workflow

If you know what you'll be workig on next, just type

    pymodoro on "Paper prototyping"

That's all. You have nothing else but your work to focus on now. And whatever you happen to think about doing just remember you have to complete the 25 minute pomodoro. Interruptions are not allowed, just work on what you wanted to work on. You'll be notified with a desktop notification (on Linux) and an audible alarm sound when the 25 minutes are gone.

What if someone interrupted you? What if you interrupted yourself? No, It work work if you allow that to happen. Some good ideas to avoid external interruptions are muting your phone or wearing earplugs. Internal interruptions (oh I have to call Alice now!) are best avoided with pencil and paper at hand. You just write it down and you keep working.

Should you be interrupted, you can log interruptions for later introspection:

    pymodoro fail

Remember, after each 25 minute pomodoro you need to take a 3-5 minute short break. You don't need an application for that. Just stand up, do some stretches or prepare some coffee, or call someone, or write some short email, etc. Sometimes you may thing that this is unnecessary. It isn't. Sometimes, when your into a hard pomodoro, you'll need to know that some fun or rest comes after the minutes left.

Finally, remember that this workflow is not suitable for everything. Sometimes you need to talk without thinking about the time, you need to get lost in time. You may also need habits, rituals, spare time. Your work shouldn't interrupt your habits, your habits shouldn't interrupt your work. Keep each of them where they belong.


### Installation

You can start using typing

    make install

It will copy Pymodoro to `/usr/local/bin` and program data to `~/.config/pymodoro`. 


### Recording



#### Activity history

* from, to, [what]
* from and to are date-times
* Once une times out a line is added
* The line means: what is being done from from to to
* Lines are never removed


#### Interruption log

* from, to, [what]
* from and to are date-times
* This is where interruptions are recorded
* Interruptions can feature what was being done
* Lines are never removed


### Reflection: what to show?

Currently the reflection feature is not implemented. I include here some ideas that could be added to Pymodoro for reflection on your work.

Proposals:
* Reflection changes depending on time of the day. Before going to bed: About tomorrow (too much stress?)

Information:
* Notify if there is agenda for today or tomorrow
* Today: What needs to be done (depending on plan)
* Today: Time available (depending on plan)
* Deadlines coming: Almost here (urgent things?)

It's coming
* Most relevant deadlines
* Relevant depends on time left and difficulty

#### Things to do. Tasks?

* task, [parent_task], [size], [done]
* a tree structure for organising tasks
* once one une is started task is added if not already there
* size is an estimator and is optional
* done is also optional, done tasks are kept for reference



### Agenda: how to organise?

* Booooh things scheduled for today (those with start and end date)
* Free time today
* Available time for work today
* Available time for work next X days


#### Plan

* [after], [before], what
* what can be a task, or something else
* either after, or before or both
* if there's only after, 43 folders style, a reminder, creator or tasks
* if there's only before, thats a deadline, deadlines are coming
* if there's box, some fixed thing ahead. Maybe a meeting. Boooh.


#### Habits

* from, to, periodicity, what, [similar_thing]
* what is never a task here
* from and to are times, not dates
* periodicity is weekly or monthly
* weekends are sacred, out of the scope
* holidays and free days and sabbatical periods are sacred, out of scope
