package com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.roomstatus;

import com.janosgyerik.meetingroomgenie.api.Reservation;

import java.util.List;

public interface StatusChangeReceiver {

    void receivedReservations(List<Reservation> reservations);

}
