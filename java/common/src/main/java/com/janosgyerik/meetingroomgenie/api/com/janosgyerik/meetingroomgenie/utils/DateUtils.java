package com.janosgyerik.meetingroomgenie.api.com.janosgyerik.meetingroomgenie.utils;

import java.util.Calendar;
import java.util.Date;

public class DateUtils {
    private DateUtils() {
        // utility class, forbidden constructor
    }

    public static Date now() {
        return Calendar.getInstance().getTime();
    }

    public static Date plusMinutes(Date date, int minutes) {
        return new Date(date.getTime() + minutes * 60 * 1000);
    }

    public static Date minusMinutes(Date date, int minutes) {
        return plusMinutes(date, -minutes);
    }
}
