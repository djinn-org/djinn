package com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.roomstatus;

import com.janosgyerik.meetingroomgenie.api.Reservation;
import org.junit.Test;

import java.util.Arrays;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;

import static org.mockito.Mockito.*;

public class StatusChangeMonitorImplTest {
    @Test
    public void test_onFree_if_no_reservations() {
        StatusChangeListener listener = mock(StatusChangeListener.class);
        StatusChangeReceiver receiver = new StatusChangeReceiverImpl(listener);
        receiver.receivedReservations(Collections.emptyList());

        verify(listener).onFree();
        verifyNoMoreInteractions(listener);
    }

    @Test
    public void test_onReserved_if_meeting_imminent() {
        StatusChangeListener listener = mock(StatusChangeListener.class);
        StatusChangeReceiver receiver = new StatusChangeReceiverImpl(listener);

        Reservation reservation = mock(Reservation.class);
        Date now = Calendar.getInstance().getTime();
        when(reservation.getStart()).thenReturn(now);
        when(reservation.getEnd()).thenReturn(now);
        receiver.receivedReservations(Arrays.asList(reservation));

        verify(listener).onReserved();
        verifyNoMoreInteractions(listener);
    }

    @Test
    public void test_onOngoing_if_during_meeting() {
        StatusChangeListener listener = mock(StatusChangeListener.class);
        StatusChangeReceiver receiver = new StatusChangeReceiverImpl(listener);

        Reservation reservation = mock(Reservation.class);
        Date now = Calendar.getInstance().getTime();
        when(reservation.getStart()).thenReturn(now);
        when(reservation.getEnd()).thenReturn(now);
        receiver.receivedReservations(Arrays.asList(reservation));

        verify(listener).onOngoing();
        verifyNoMoreInteractions(listener);
    }

}