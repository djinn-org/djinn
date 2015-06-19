package com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.roomstatus;

import com.janosgyerik.meetingroomgenie.api.Reservation;
import com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.utils.DateUtils;

import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class StatusChangeReceiverImpl implements StatusChangeReceiver {

    protected static final int MINUTES_TO_WARN_BEFORE_NEXT_RESERVATION = 15;
    protected static final int MINUTES_OF_LONG_FREE_PERIOD = 60;

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
            Date now = DateUtils.now();

            Date end = reservation.getEnd();

            // sanity check
            if (now.after(end)) {
                return;
            }

            Date start = reservation.getStart();
            Date longFreeLimit = DateUtils.minusMinutes(start, MINUTES_OF_LONG_FREE_PERIOD);
            Date startReservationLimit = DateUtils.minusMinutes(start, MINUTES_TO_WARN_BEFORE_NEXT_RESERVATION);
            Date endReservationLimit = DateUtils.minusMinutes(end, MINUTES_TO_WARN_BEFORE_NEXT_RESERVATION);

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
}
