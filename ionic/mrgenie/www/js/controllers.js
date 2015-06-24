angular.module('mrgenie.controllers', [])

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

        function to_local_date(date) {
            return new Date(new Date() + 1000 * 60 * 60 * 2)
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
                        var start_date = to_date_today(item.start_date);
                        var end_date = to_date_today(item.end_date);
                        return to_hhmm(start_date) + ' - ' + to_hhmm(end_date);
                    });
                $scope.reservations = times.map(function (time) { return {time: time}; });

                var time_as_int = parseInt($stateParams.time);
                var time = isNaN(time_as_int) ? to_local_date(new Date()) : from_hhmm(time_as_int);
                $scope.time = time;

                $scope.status = get_status(reservations, time);
            });
        });
    })
;
