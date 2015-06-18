package com.janosgyerik.meetingroomgenie.api;

import java.util.List;

public interface ReservationManager {

    List<Reservation> getReservations(RoomId roomId);

    void sendValidation(RoomId roomId);

    List<Room> getRooms();
}
