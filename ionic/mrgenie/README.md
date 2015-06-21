Ionic
-----

Useful commands:

    ionic start todoApp tabs
    ionic platform add android
    ionic build android
    ionic run android
    ionic emulate android

http://ionicframework.com/getting-started/


Parse
-----

Working with parse.com and Ionic:

http://www.htmlxprs.com/post/12/tutorial-on-using-parse-rest-api-and-ionic-framework-together

Creating relations on parse.com:

- Given a custom class `Room`
- Given a custom class `Reservation`
  + with column: `room<Relation>`

Example commands:

    curl -X PUT -H "X-Parse-Application-Id: tdhNUXe5ytcL28D4e0hv5782fFw0N6iFkIS7Tiyn" -H "X-Parse-REST-API-Key: aoi46j5L12B2o1pNmGzceCSTj3cyzgGb5nK8uPzA" -H "Content-Type: application/json" -d '{"room":{"__op":"AddRelation","objects":[{"__type":"Pointer","className":"Room","objectId":"eU9npkV8mZ"}]}}' https://api.parse.com/1/classes/Reservation/pVTq4Wdw74
    curl -X PUT -H "X-Parse-Application-Id: tdhNUXe5ytcL28D4e0hv5782fFw0N6iFkIS7Tiyn" -H "X-Parse-REST-API-Key: aoi46j5L12B2o1pNmGzceCSTj3cyzgGb5nK8uPzA" -H "Content-Type: application/json" -d '{"room":{"__op":"AddRelation","objects":[{"__type":"Pointer","className":"Room","objectId":"eU9npkV8mZ"}]}}' https://api.parse.com/1/classes/Reservation/RqHo6r7KRM
    
https://www.parse.com/questions/how-can-i-add-objects-to-a-relation