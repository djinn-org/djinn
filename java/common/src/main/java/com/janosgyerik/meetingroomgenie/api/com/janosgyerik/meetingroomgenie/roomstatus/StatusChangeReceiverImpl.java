package com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.roomstatus;

import com.janosgyerik.meetingroomgenie.api.Reservation;

import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class StatusChangeReceiverImpl implements StatusChangeReceiver {

    protected static final int START_RESERVATION_WARNING_PERIOD = 15 * 60 * 1000;
    protected static final int END_RESERVATION_WARNING_PERIOD = 15 * 60 * 1000;
    protected static final int LONG_FREE_PERIOD = 60 * 60 * 1000;

    private final StatusChangeListener listener;

    public StatusChangeReceiverImpl(StatusChangeListener listener) {
        this.listener = listener;
    }

    @Override
    public void receivedReservations(List<Reservation> reservations) {
        if (reservations.isEmpty()) {
            listener.onFree();
        } else {
            Reservation reservation = reservations.get(0);
            Date now = Calendar.getInstance().getTime();

            Date end = reservation.getEnd();

            // sanity check
            if (now.after(end)) {
                return;
            }

            Date start = reservation.getStart();
            Date longFreeLimit = dateMinusPeriod(start, LONG_FREE_PERIOD);
            Date startReservationLimit = dateMinusPeriod(start, START_RESERVATION_WARNING_PERIOD);
            Date endReservationLimit = dateMinusPeriod(end, END_RESERVATION_WARNING_PERIOD);

            if (start.before(longFreeLimit)) {
                listener.onFree();
            } else if (now.before(start) && now.after(startReservationLimit)) {
                listener.onReserved();
            } else if (now.after(start)) {
                if (now.before(endReservationLimit)) {
                    listener.onOngoing();
                } else {
                    listener.onOngoingAndReserved();
                }
            }
        }
    }

    private Date dateMinusPeriod(Date date, int millis) {
        return new Date(date.getTime() - millis);
    }
}
