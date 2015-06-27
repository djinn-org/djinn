Overview
========

Simple high-level overview of the project idea.

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

### Problem 2: booking a room is not driven by the needs of users

When booking a room, users have very common and very natural needs:

- Capacity: the number of chairs
- Equipment: PC, phone, whiteboard, or other
- Proximity: close to the organizer, or to the majority of participants,
  or to the most important stakeholders

The current booking system is not oriented around these simple needs.
The current booking system is very far from helping users to book a room.
Finding a suitable room is a non-trivial, often time-consuming task,
and it shouldn't be that way.

### Problem 3: cases of booked but unused rooms

Sometimes a room is booked but not used, because the meeting was canceled,
but not the room booking. This is very unfortunate, as the perfect room
might appear unavailable to users who really need it.

### Problem 4: no visible indication of the room status during a meeting

Sometimes meetings exceed their planned duration, and when the new users who
booked the next time slot arrive are in the awkward situation that they
either have to wait for the previous group to get out, or to be rude to
force them out.

It would be good to have a system to signal to the current users of the room
that they need to wrap up their meeting soon, to give way to the next group.
Or even better, automatically extend the booking if the room is still
available, or find another meeting room, preferably nearby, to continue
after the current time slot expires.

### Problem 5: missing features that would be obviously useful

For example:

- When you step into an empty meeting room, it would be nice to be able to book it

- It would be nice to have a status display in every room,
  indicating the given day's schedule
