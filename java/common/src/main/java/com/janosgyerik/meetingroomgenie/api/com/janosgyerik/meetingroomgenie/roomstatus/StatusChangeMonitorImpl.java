package com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.roomstatus;

import com.janosgyerik.meetingroomgenie.api.Reservation;
import com.janosgyerik.meetingroomgenie.api.ReservationManager;
import com.janosgyerik.meetingroomgenie.api.RoomId;

import java.util.List;

public class StatusChangeMonitorImpl implements StatusChangeMonitor {

    private final ReservationManager manager;

    StatusChangeMonitorImpl(ReservationManager manager) {
        this.manager = manager;
    }

    private void pollServer(RoomId roomId) {
        List<Reservation> reservations = manager.getReservations(roomId);
        if (reservations.isEmpty()) {
        }
    }

    @Override
    public void subscribe(RoomId roomId, StatusChangeListener listener) {

    }

    @Override
    public void unsubscribe(RoomId roomId, StatusChangeListener listener) {

    }
}
