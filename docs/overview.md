Overview
========

Explanation of the problems related to booking meeting rooms,
and the proposed solutions to solve or mitigate the problems.

The problems
------------

There are several problems around the current meeting room booking system.

### Problem 1: booking a room is too complicated

The current process to book a room is not easy, and not natural:

1. Open the screen to organize a meeting, and select the option to add rooms

2. Read the list of rooms, select some candidates based on the listed floor number and capacity

3. Add the selected rooms to the meeting, and remove the ones that are not available

4. Choose one of the remaining rooms

One big problem is that it's impossible to know the equipment in the rooms,
and there is no way to filter by available equipment, such as PC, whiteboard, phone.

Another big problem is that reading the full list of rooms,
scanning with our eyes for the required floor and capacity is inconvenient and error prone.

The current system becomes easier to use when you know the rooms by heart:
when you know their names to find them in the list easily,
and you know what capacity and equipment they have.
But even then, if your favorite meeting rooms are all taken,
your frustration will be just as great as when trying to book your first meeting ever.

### Problem 2: the process of booking a room is not user-oriented

When booking a room, users have very common and very natural needs:

- Capacity: the number of chairs
- Equipment: PC, phone, whiteboard, or other
- Proximity: close to the organizer, or to the majority of participants,
  or to the most important stakeholders

The current booking system is not oriented around these simple needs.
The current booking system is very far from helping users to book a room.
Finding a suitable room is a non-trivial, often time-consuming task,
and it shouldn't be that way.

### Problem 3: many booked but unused rooms

Sometimes a room is booked but not used, because the meeting was canceled,
but not the room booking. This is very unfortunate, as the perfect room
might appear unavailable to users who really need it.

### Problem 4: many meetings exceed their booking and cause delay for others

Sometimes meetings exceed their planned duration, and when the new users who
booked the next time slot arrive are in the awkward situation that they
either have to wait for the previous group to get out, or to be rude to
force them out.

It would be good to have a system to signal to the current users of the room
that they need to wrap up their meeting soon, to give way to the next group.
Or even better, automatically extend the booking if the room is still
available, or find another meeting room, preferably nearby, to continue
after the current time slot expires.

### Problem 5: missing obvious features

For example:

- When you step into an empty meeting room, it would be nice to be able to book it

- It would be nice to have a status display in every room,
  indicating the schedule of the given day

### Problem 6 (to delete): available rooms that are not really available

Sometimes a meeting room is marked as available in the current system,
but in reality there are users inside. When the users who booked the time slot
arrive, they find themselves in the awkward situation that they
either have to wait for the "illegal" group to get out, or to be rude to
force them out.

@Matthieu: this problem seems too rare, and much less significant than the others.
If you don't mind, I think we should drop this.

The solution
------------

We propose a system that is user-oriented, driven by the natural needs of users,
and addresses the above problems.

### Part 1: ergonomic user interface

Booking a room should be possible using a simple, ergonomic user interface:

1. The user specifies the requirements:
  + Meeting time and duration
  + Capacity: the number of chairs
  + Equipment: PC, phone, whiteboard, ...
  + Proximity: close to the organizer by default
    - Optionally: close to the majority of participants
    - Optionally: close to selected participants

2. The system offers matching choices, ordered by how closely they match
   the specified requirements

3. The user selects a room

This solves two problems:

- Problem 1: booking a room is too complicated

- Problem 2: the process of booking a room is not user-oriented

As an added bonus, for easy access, a unified user interface should be available
on multiple platforms, such as:

- Mobile phone app (Android, iPhone, Windows)
- Web interface
- Smart watch

### Part 2: reduce the number of booked but unused rooms

The system should detect rooms that are booked but unused:

- Users of a room should "check-in", using a mechanism (TODO)
  that requires physical presence, for example an employee badge
  placed on some sort of docking station (TODO)

- When the physical device used to check-in leaves the room,
  the booking should be canceled immediately

- The system should check for bookings in progress that haven't
  received a check-in signal, and handle gracefully.
  For example, alert the organizer that the booking will be
  canceled within a few minutes. The organizer may request
  to extend the deadline briefly.

This solves Problem 3: many booked but unused rooms

### Part 3: provide a status indicator device each room

The status indicator will have the following states:

- Available: green light, if not booked at the moment,
  and for the next 15 minutes (configurable)

- Reserved: blue light, if a booking is about to start
  within 15 minutes (configurable)

- Occupied: red light, if a meeting is in progress,
  and there is no other booking for the next 15 minutes

The Reserved status is the most important:
during a meeting in progress, it signals to users
that they need to wrap up their talk, and thereby avoid
conflicts with the next group that will come to the room.
In such situation, the users may want to find another room
to continue. The system should make it easy to find
a similar room with the same search criteria used for the current one.

This should mitigate Problem 4: many meetings exceed their booking and cause delay for others

### Part 4: additional useful features

For example:

- The system should provide an easy way to book the current room right now,
  if the room is available

- There should be a status display in every room,
  indicating the schedule of the given day
