var STATUS_FREE = 'FREE';
var STATUS_RESERVED = 'RESERVED';
var STATUS_MEETING = 'MEETING';

var PENDING_RESERVATION_TIMEDELTA = from_minutes(15);


function from_minutes(minutes) {
    return minutes * 60 * 1000;
}

function from_hours(hours) {
    return from_minutes(60);
}

function from_days(days) {
    return from_hours(24);
}

// this is for easier working with test data
function to_date_today(parse_api_date) {
    var date = new Date(Date.parse(parse_api_date.iso));
    var today = new Date();
    today.setHours(date.getHours());
    today.setMinutes(date.getMinutes());
    today.setSeconds(0);
    return today;
}

function to_hhmm(date) {
    function pad(num) {
        return num < 10 ? '0' + num : num;
    }
    return pad(date.getHours()) + ':' + pad(date.getMinutes());
}

function from_hhmm(time) {
    var date = new Date();
    date.setHours(time % 10000 / 100);
    date.setMinutes(time % 100);
    return date;
}

function get_status(reservations0, time) {
    var reservations1 = reservations0.map(function (item) {
        return {
            start_date: to_date_today(item.start_date),
            end_date: to_date_today(item.end_date)
        };
    });
    var reservations = get_relevant_reservations(get_clean_reservations(reservations1), time)
        .sort(function (r1, r2) { return r1.start_date >= r2.start_date; });

    var timeline = [];
    for (var i = 0; i < reservations.length; ++i) {
        var reservation = reservations[i];
        var pending_date = plus_timedelta(reservation.start_date, -PENDING_RESERVATION_TIMEDELTA);
        timeline.push({status: STATUS_RESERVED, time: pending_date});
        timeline.push({status: STATUS_MEETING, time: reservation.start_date});

        if (i + 1 < reservations.length) {
            var next_reservation = reservations[i + 1];
            var next_pending_date = plus_timedelta(next_reservation.start_date, -PENDING_RESERVATION_TIMEDELTA);
            if (reservation.end_date < next_pending_date) {
                timeline.push({status: STATUS_FREE, time: reservation.end_date});
            }
        }
    }

    var status = STATUS_FREE;
    for (i = 0; i < timeline.length; ++i) {
        var entry = timeline[i];
        if (time < entry.time) {
            return status;
        }
        status = entry.status;
    }
    return status;
}

function get_clean_reservations(reservations) {
    return reservations.filter(function (item) {
        return item.start_date && item.end_date && item.end_date > item.start_date;
    });
}

function get_relevant_reservations(reservations, time) {
    return reservations.filter(function (item) {
        return time < item.end_date && plus_timedelta(item.start_date, -PENDING_RESERVATION_TIMEDELTA) <= time;
    });
}

function plus_timedelta(date, timedelta) {
    return new Date(date.getTime() + timedelta);
}