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

	public static JSONObject appointmentToJSON(Appointment appointment) throws Exception {

		return new JSONObject()
				.put("start", appointment.getStart())
				.put("end", appointment.getEnd());
	}

}
