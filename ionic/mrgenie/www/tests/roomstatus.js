test('free if empty', function () {
    equal(STATUS_FREE, get_status([]));
    equal(STATUS_FREE, get_status([], new Date()));
});

test('free if no meeting soon', function () {
    var now = new Date();
    var start_date = plus_timedelta(now, PENDING_RESERVATION_TIMEDELTA + 1);
    var end_date = plus_timedelta(start_date, 1);
    var reservations = [{start_date: start_date, end_date: end_date}];
    equal(STATUS_FREE, get_status(reservations, now));
});

test('reserved if meeting soon', function () {
    var now = new Date();
    var start_date = plus_timedelta(now, PENDING_RESERVATION_TIMEDELTA - from_minutes(1));
    var end_date = plus_timedelta(start_date, 1);
    var reservations = [{start_date: start_date, end_date: end_date}];
    equal(STATUS_RESERVED, get_status(reservations, now));
});

test('meeting in progress', function () {
    var now = new Date();
    var start_date = plus_timedelta(now, -from_minutes(1));
    var end_date = plus_timedelta(now, from_minutes(1));
    var reservations = [{start_date: start_date, end_date: end_date}];
    equal(STATUS_MEETING, get_status(reservations, now));
});

test('meeting in progress if next meeting much later', function () {
    var now = new Date();
    var start_date = plus_timedelta(now, -from_minutes(1));
    var end_date = plus_timedelta(now, from_minutes(1));
    var start_date2 = plus_timedelta(end_date, PENDING_RESERVATION_TIMEDELTA + from_minutes(1));
    var end_date2 = plus_timedelta(start_date2, from_minutes(1));
    var reservations = [
        {start_date: start_date, end_date: end_date},
        {start_date: start_date2, end_date: end_date2}
    ];
    equal(STATUS_MEETING, get_status(reservations, now));
});

test('reserved if next meeting soon', function () {
    var now = new Date();
    var start_date = plus_timedelta(now, -from_minutes(1));
    var end_date = plus_timedelta(now, from_minutes(1));
    var start_date2 = plus_timedelta(now, PENDING_RESERVATION_TIMEDELTA - from_minutes(1));
    var end_date2 = plus_timedelta(start_date2, from_minutes(1));
    var reservations = [
        {start_date: start_date, end_date: end_date},
        {start_date: start_date2, end_date: end_date2}
    ];
    equal(STATUS_RESERVED, get_status(reservations, now));
});

test('clean reservations: empty if empty', function () {
    equal(0, get_clean_reservations([]).length);
});

test('clean reservations: empty if start_date missing', function () {
    equal(0, get_clean_reservations([{end_date: new Date()}]).length);
});

test('clean reservations: empty if end_date missing', function () {
    equal(0, get_clean_reservations([{start_date: new Date()}]).length);
});

test('clean reservations: empty if start_date == end_date', function () {
    equal(0, get_clean_reservations([{start_date: new Date(), end_date: new Date()}]).length);
});

test('clean reservations: ok if start_date + end_date both present', function () {
    var start_date = new Date(new Date().getTime() - 1);
    equal(1, get_clean_reservations([{start_date: start_date, end_date: new Date()}]).length);
});

test('relevant reservations: empty if ends before time', function () {
    var now = new Date();
    var start_date = plus_timedelta(now, -10);
    var end_date = plus_timedelta(now, -1);
    var reservations = [{start_date: start_date, end_date: end_date}];
    equal(1, get_clean_reservations(reservations).length);
    equal(0, get_relevant_reservations(reservations, now).length);
});

test('relevant reservations: empty if starts much later', function () {
    var now = new Date();
    var start_date = plus_timedelta(now, PENDING_RESERVATION_TIMEDELTA + 1);
    var end_date = plus_timedelta(start_date, 1);
    var reservations = [{start_date: start_date, end_date: end_date}];
    equal(1, get_clean_reservations(reservations).length);
    equal(0, get_relevant_reservations(reservations, now).length);
});

test('relevant reservations: ok if starts soon', function () {
    var now = new Date();
    var start_date = plus_timedelta(now, PENDING_RESERVATION_TIMEDELTA - from_minutes(1));
    var end_date = plus_timedelta(start_date, 1);
    var reservations = [{start_date: start_date, end_date: end_date}];
    equal(1, get_clean_reservations(reservations).length);
    equal(1, get_relevant_reservations(reservations, now).length);
});
