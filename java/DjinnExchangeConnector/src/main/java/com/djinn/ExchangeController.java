package com.djinn;

import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import microsoft.exchange.webservices.data.core.service.folder.CalendarFolder;
import microsoft.exchange.webservices.data.core.service.item.Appointment;
import microsoft.exchange.webservices.data.core.service.item.EmailMessage;
import microsoft.exchange.webservices.data.property.complex.MessageBody;
import microsoft.exchange.webservices.data.search.CalendarView;
import microsoft.exchange.webservices.data.search.FindItemsResults;
import org.json.JSONObject;

public class ExchangeController {

	private static ExchangeController instance = null;

	private ConnectionManager manager = null;

	private ExchangeController() throws URISyntaxException {
		this.manager = ConnectionManager.getInstance();

	}

	public static ExchangeController getInstance() throws URISyntaxException {
		if (instance == null)
			instance = new ExchangeController();

		return instance;
	}

	public static ExchangeController getInstanceOrDie() {
		try {
			return new ExchangeController();
		} catch (URISyntaxException e) {
			e.printStackTrace();
			System.exit(1);
		}
		throw new AssertionError("Unreachable statement");
	}

	public void sendEmail(String subject, String msgBody, List<String> listDestination) throws Exception {
		EmailMessage msg = manager.getNewEmail();

		msg.setSubject(subject);
		msg.setBody(MessageBody.getMessageBodyFromText(msgBody));

		for (String destination : listDestination) {
			msg.getToRecipients().add(destination);
		}

		msg.send();
	}

	/**
	 * Make a meeting
	 *
	 * @param startDate  format = yyyy-MM-dd HH:mm:ss
	 * @param endDate    format = yyyy-MM-dd HH:mm:ss
	 * @param location   might be null I know it's not clean, It's quick and dirty...
	 * @param onBehalfOf might be null
	 */
	public int makeAMeeting(String subject, String body, String startDate, String endDate, String location, String onBehalfOf) {
		try {
			//TODO : test parameters...

			Appointment appointment = manager.getNewappointment();

			appointment.setSubject(subject);
			appointment.setBody(MessageBody.getMessageBodyFromText(body));

			Date startDat = ToolBox.formatDate(startDate);
			Date endDat = ToolBox.formatDate(endDate);

			appointment.setStart(startDat);
			appointment.setEnd(endDat);

			//set location is simple text, does not send an invitation to the room
			if (location == null)
				location = "";
			appointment.setLocation(location);
			appointment.getRequiredAttendees().add(location + "@" + ConfigManager.getMailDomain());

			if (onBehalfOf == null || onBehalfOf.isEmpty())
				appointment.save();
			else
				appointment.save(manager.getSomeoneFolderId(onBehalfOf));

			return 0;
		} catch (Exception e) {
			e.printStackTrace();
			return 1;
		}
	}

	private FindItemsResults<Appointment> getAppointments(String startDate, String endDate, String onBehafOf) throws Exception {
		CalendarFolder cf;
		if (onBehafOf.equals(ConfigManager.getUsername())) {
			cf = this.manager.getMyCalendar();
		} else {
			cf = this.manager.getSomeoneCalendar(onBehafOf);
		}

		CalendarView cv = this.manager.getNewCalendarView(startDate, endDate);

		return cf.findAppointments(cv);
	}

	public JSONObject findMyAppointments(String startDate, String endDate) throws Exception {
		return findAppointments(startDate, endDate, ConfigManager.getUsername());
	}

	public JSONObject findSomeoneAppointments(String startDate, String endDate, String user) throws Exception {
		return findAppointments(startDate, endDate, user);
	}

	private JSONObject findAppointments(String startDate, String endDate, String onBehafOf) throws Exception {
		ArrayList<String> users = new ArrayList<>();
		users.add(onBehafOf);

		return findManyUserAppointments(startDate, endDate, users);
	}

	public JSONObject findManyUserAppointments(String startDate, String endDate, ArrayList<String> users) throws Exception {

		JSONObject json = new JSONObject();

		for (String onBehafOf : users) {
			ArrayList<JSONObject> listOfJSONAppointment = new ArrayList<>();

			for (Appointment appointment : getAppointments(startDate, endDate, onBehafOf)) {
				listOfJSONAppointment.add(ToolBox.appointmentToJSON(appointment));
			}
			if (!listOfJSONAppointment.isEmpty())
				json.put(onBehafOf, listOfJSONAppointment);
		}

		return json;
	}

	public int declineMyAppointments(String startDate, String endDate) {
		try {

			this.decline(this.getAppointments(startDate, endDate, ConfigManager.getUsername()));
			return 0;

		} catch (Exception e) {
			e.printStackTrace();
			return 1;
		}
	}

	public int declineAppointmentsOnBehalfOf(String startDate, String endDate, String onBehafOf) {
		try {

			this.decline(this.getAppointments(startDate, endDate, onBehafOf));
			return 0;

		} catch (Exception e) {
			e.printStackTrace();
			return 1;
		}
	}

	private int decline(FindItemsResults<Appointment> appointments) throws Exception {
		int cpt = 0;
		for (Appointment appt : appointments.getItems()) {
			//TODO handle logs
			//System.out.println("SUBJECT of appoint to decline====="+appt.getSubject());
			appt.decline(true);
			cpt++;
		}

		return cpt;
	}

	public void close() {
		this.manager.close();
	}

}
