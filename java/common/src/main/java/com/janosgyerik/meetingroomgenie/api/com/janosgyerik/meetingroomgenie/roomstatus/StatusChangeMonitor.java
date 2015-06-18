package com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.roomstatus;

import com.janosgyerik.meetingroomgenie.api.RoomId;

public interface StatusChangeMonitor {

    void subscribe(RoomId roomId, StatusChangeListener listener);

    void unsubscribe(RoomId roomId, StatusChangeListener listener);

}
