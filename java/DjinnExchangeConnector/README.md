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