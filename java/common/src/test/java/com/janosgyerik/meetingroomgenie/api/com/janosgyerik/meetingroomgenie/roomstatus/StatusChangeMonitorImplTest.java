package com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.roomstatus;

import com.janosgyerik.meetingroomgenie.api.Reservation;
import com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.utils.DateUtils;
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
    public void test_onFree_if_no_reservations_soon() {
        StatusChangeListener listener = mock(StatusChangeListener.class);
        StatusChangeReceiver receiver = new StatusChangeReceiverImpl(listener);
        receiver.receivedReservations(Collections.emptyList());

        Reservation reservation = mock(Reservation.class);
        Date now = Calendar.getInstance().getTime();
        Date muchLater = DateUtils.plusMinutes(now, StatusChangeReceiverImpl.MINUTES_OF_LONG_FREE_PERIOD);
        Date muchLaterEnd = DateUtils.plusMinutes(muchLater, 10);

        when(reservation.getStart()).thenReturn(muchLater);
        when(reservation.getEnd()).thenReturn(muchLaterEnd);
        receiver.receivedReservations(Arrays.asList(reservation));

        verify(listener).onFree();
        verifyNoMoreInteractions(listener);
    }

    @Test
    public void test_onReserved_if_meeting_imminent() {
        StatusChangeListener listener = mock(StatusChangeListener.class);
        StatusChangeReceiver receiver = new StatusChangeReceiverImpl(listener);

        Reservation reservation = mock(Reservation.class);
        Date now = Calendar.getInstance().getTime();
        Date nextMeeting = DateUtils.plusMinutes(
                now, StatusChangeReceiverImpl.MINUTES_TO_WARN_BEFORE_NEXT_RESERVATION - 1);
        when(reservation.getStart()).thenReturn(nextMeeting);
        when(reservation.getEnd()).thenReturn(nextMeeting);
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
        Date started = DateUtils.minusMinutes(now, 1);
        Date endLater = DateUtils.plusMinutes(
                now, StatusChangeReceiverImpl.MINUTES_TO_WARN_BEFORE_NEXT_RESERVATION + 1);
        when(reservation.getStart()).thenReturn(started);
        when(reservation.getEnd()).thenReturn(endLater);
        receiver.receivedReservations(Arrays.asList(reservation));

        verify(listener).onOngoing();
        verifyNoMoreInteractions(listener);
    }

}