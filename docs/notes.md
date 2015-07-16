Notes
=====

Real-time updates
-----------------

Technologies to get status updates from the server in real time:

- Web sockets: 2-way communication between server and client
- Long polling: server waits until there is a change in status
- [Server sent events][2]: server sends messages when there is a change status

See this informative [discussion][1].

Real-time updates with Ionic
----------------------------

- [Writing an AngularJS App with Socket.IO](http://www.html5rocks.com/en/tutorials/frameworks/angular-websockets/)

[1]: http://stackoverflow.com/questions/11077857/what-are-long-polling-websockets-server-sent-events-sse-and-comet
[2]: https://en.wikipedia.org/wiki/Server-sent_events
