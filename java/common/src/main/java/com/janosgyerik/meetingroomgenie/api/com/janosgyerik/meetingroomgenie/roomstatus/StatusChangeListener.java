package com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.roomstatus;

public interface StatusChangeListener {

    void onFree();

    void onReserved();

    void onOngoing();

    void onOngoingAndReserved();

    void onValidationRequested();
}
