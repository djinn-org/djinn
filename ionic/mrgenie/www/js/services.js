angular.module('starter.services', [])

    .factory('Chats', function () {
        // Might use a resource here that returns a JSON array

        // Some fake testing data
        var chats = [{
            id: 0,
            name: 'Ben Sparrow',
            lastText: 'You on your way?',
            face: 'https://pbs.twimg.com/profile_images/514549811765211136/9SgAuHeY.png'
        }, {
            id: 1,
            name: 'Max Lynx',
            lastText: 'Hey, it\'s me',
            face: 'https://avatars3.githubusercontent.com/u/11214?v=3&s=460'
        }, {
            id: 4,
            name: 'Mike Harrington',
            lastText: 'This is wicked good ice cream.',
            face: 'https://pbs.twimg.com/profile_images/578237281384841216/R3ae1n61.png'
        }];

        return {
            all: function () {
                return chats;
            },
            remove: function (chat) {
                chats.splice(chats.indexOf(chat), 1);
            },
            get: function (chatId) {
                for (var i = 0; i < chats.length; i++) {
                    if (chats[i].id === parseInt(chatId)) {
                        return chats[i];
                    }
                }
                return null;
            }
        };
    })
    .factory('Room', ['$http', 'PARSE_CREDENTIALS', function ($http, PARSE_CREDENTIALS) {
        function getAll() {
            return $http.get('https://api.parse.com/1/classes/Room', {
                headers: {
                    'X-Parse-Application-Id': PARSE_CREDENTIALS.APP_ID,
                    'X-Parse-REST-API-Key': PARSE_CREDENTIALS.REST_API_KEY
                }
            });
        }
        return {
            getAll: getAll,
            get: function (id) {
                return $http.get('https://api.parse.com/1/classes/Room/' + id, {
                    headers: {
                        'X-Parse-Application-Id': PARSE_CREDENTIALS.APP_ID,
                        'X-Parse-REST-API-Key': PARSE_CREDENTIALS.REST_API_KEY
                    }
                });
            }
        }
    }])
    .factory('Reservation', ['$http', 'PARSE_CREDENTIALS', function ($http, PARSE_CREDENTIALS) {
        function getAll() {
            return $http.get('https://api.parse.com/1/classes/Reservation', {
                headers: {
                    'X-Parse-Application-Id': PARSE_CREDENTIALS.APP_ID,
                    'X-Parse-REST-API-Key': PARSE_CREDENTIALS.REST_API_KEY
                }
            });
        }
        return {
            getAll: getAll,
            query: function (objectId) {
                return $http.get('https://api.parse.com/1/classes/Reservation', {
                    headers: {
                        'X-Parse-Application-Id': PARSE_CREDENTIALS.APP_ID,
                        'X-Parse-REST-API-Key': PARSE_CREDENTIALS.REST_API_KEY
                    },
                    params: {
                        where: {
                            room: {
                                __type: 'Pointer',
                                className: 'Room',
                                objectId: objectId
                            }
                        }
                    }
                });
            }
        }
    }])
    .value('PARSE_CREDENTIALS', {
        APP_ID: 'tdhNUXe5ytcL28D4e0hv5782fFw0N6iFkIS7Tiyn',
        REST_API_KEY: 'aoi46j5L12B2o1pNmGzceCSTj3cyzgGb5nK8uPzA'
    })
;
