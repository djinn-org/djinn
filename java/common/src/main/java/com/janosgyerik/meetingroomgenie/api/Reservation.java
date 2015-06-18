package com.janosgyerik.meetingroomgenie.api;

import java.util.Date;
import java.util.List;

public interface Reservation {

    Date getStart();

    Date getEnd();

    User getOrganizer();

    List<User> getParticipants();

    String getSubject();

}
