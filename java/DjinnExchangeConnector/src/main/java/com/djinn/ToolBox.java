package com.djinn;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

import microsoft.exchange.webservices.data.core.service.item.Appointment;
import org.json.JSONObject;

public class ToolBox {

	public static Date parseDate(String date) {
		SimpleDateFormat formatter = new SimpleDateFormat(ConnectionManager.dateFormat);
		try {
			return formatter.parse(date);
		} catch (ParseException e) {
			return null;
		}
	}

	private static String formatDate(Date date) {
		return new SimpleDateFormat("yyyy-MM-dd HH:mm").format(date);
	}

	public static JSONObject appointmentToJSON(Appointment appointment) throws Exception {
		return new JSONObject()
				.put("start", formatDate(appointment.getStart()))
				.put("end", formatDate(appointment.getEnd()));
	}

}
