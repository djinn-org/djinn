angular.module('mrgenie.services', [])

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
