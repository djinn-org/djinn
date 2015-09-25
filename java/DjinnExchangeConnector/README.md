Exchange connector
==================

TODO

Building
--------

The project depends on an external artifact. Clone and install:

	git clone https://github.com/OfficeDev/ews-java-api.git
	cd ews-java-api
	mvn install
	
After this a simple build should work:

	mvn compile

Packaging
---------

To pack up the entire project in a self-contained jar:

	mvn assembly:single
	
This will generate: `target/*-jar-with-dependencies.jar`

Usage
-----

List reservations for Room1 and Room2 between September 25, 15:30 and 19:00:  

    java -cp target/TestEWS-0.0.1-SNAPSHOT-jar-with-dependencies.jar com.djinn.run.ListReservations 201509251530 201509251900 Room1 Room2

Create a reservation for Room1 between September 25, 16:30 and 17:00:  

    java -cp target/TestEWS-0.0.1-SNAPSHOT-jar-with-dependencies.jar com.djinn.run.CreateReservation 201509251630 201509251700 Room1
