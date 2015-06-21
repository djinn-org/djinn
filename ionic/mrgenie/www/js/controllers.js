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
                var reservations = data.results;

                var times = data.results
                    .map(function (item) {
                        var start_date = to_date(item.start_date);
                        var end_date = to_date(item.end_date);
                        return to_hhmm(start_date) + ' - ' + to_hhmm(end_date);
                    });
                $scope.reservations = times.map(function (time) { return {time: time}; });

                var now = new Date();
                //now = new Date(Date.parse("2015-06-21T17:50:00.000Z"));
                $scope.status = get_status(reservations, now);
            });
        });
    })
;
