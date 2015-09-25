package com.djinn;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

import microsoft.exchange.webservices.data.core.service.item.Appointment;
import org.json.JSONObject;

public class ToolBox {

	public static Date formatDate(String date) throws ParseException {
		SimpleDateFormat formatter = new SimpleDateFormat(ConnectionManager.dateFormat);
		return formatter.parse(date);
	}

	public static JSONObject appointmentToJSON(Appointment appointment) throws Exception {

		return new JSONObject()
				.put("start", appointment.getStart())
				.put("end", appointment.getEnd());
	}

}
