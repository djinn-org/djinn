angular.module('starter.controllers', [])

    .controller('RoomListController', ['$scope', 'Room', function ($scope, Room) {
        Room.getAll().success(function (data) {
            $scope.rooms = data.results;
        });
    }])

    .controller('RoomController', function ($scope, $stateParams, Room, Reservation) {
        function getRoom(rooms, name) {
            for (var i = 0; i < rooms.length; ++i) {
                var room = rooms[i];
                if (room.name == name) {
                    return room;
                }
            }

            if (rooms.length > 0) {
                return rooms[0];
            }
        }

        Room.getAll().success(function (data) {
            var rooms = data.results;
            var room = getRoom(rooms, $stateParams.name);
            if (!room) {
                $scope.room = {name: '?'};
                return;
            }

            $scope.room = room;

            Reservation.query($scope.room.objectId).success(function (data) {
                $scope.reservations = data.results
                    .map(function (item) {
                        var start_date = item.start_date.iso;
                        var time = start_date.substr(start_date.indexOf('T') + 1, 5);
                        return {'time': time};
                    });
            });
        });
    })
;
