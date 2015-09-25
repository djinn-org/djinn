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
	public boolean makeAMeeting(String subject, String body, Date startDate, Date endDate, String location, String onBehalfOf) {
		try {
			//TODO : test parameters...

			Appointment appointment = manager.getNewappointment();

			appointment.setSubject(subject);
			appointment.setBody(MessageBody.getMessageBodyFromText(body));
			appointment.setStart(startDate);
			appointment.setEnd(endDate);

			//set location is simple text, does not send an invitation to the room
			if (location == null)
				location = "";
			appointment.setLocation(location);
			appointment.getRequiredAttendees().add(location + "@" + ConfigManager.getMailDomain());

			if (onBehalfOf == null || onBehalfOf.isEmpty())
				appointment.save();
			else
				appointment.save(manager.getSomeoneFolderId(onBehalfOf));

			return true;
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}

	private FindItemsResults<Appointment> getAppointments(Date startDate, Date endDate, String onBehafOf) throws Exception {
		CalendarFolder cf;
		if (onBehafOf.equals(ConfigManager.getUsername())) {
			cf = this.manager.getMyCalendar();
		} else {
			cf = this.manager.getSomeoneCalendar(onBehafOf);
		}

		CalendarView cv = this.manager.getNewCalendarView(startDate, endDate);

		return cf.findAppointments(cv);
	}

	public JSONObject findMyAppointments(Date startDate, Date endDate) throws Exception {
		return findAppointments(startDate, endDate, ConfigManager.getUsername());
	}

	public JSONObject findSomeoneAppointments(Date startDate, Date endDate, String user) throws Exception {
		return findAppointments(startDate, endDate, user);
	}

	private JSONObject findAppointments(Date startDate, Date endDate, String onBehafOf) throws Exception {
		ArrayList<String> users = new ArrayList<>();
		users.add(onBehafOf);

		return findManyUserAppointmentsJSON(startDate, endDate, users);
	}

	public String findManyUserAppointments(Date startDate, Date endDate, List<String> users) throws Exception {
		return findManyUserAppointmentsJSON(startDate, endDate, users).toString(5);
	}

	public JSONObject findManyUserAppointmentsJSON(Date startDate, Date endDate, List<String> users) throws Exception {

		JSONObject json = new JSONObject();

		for (String onBehafOf : users) {
			List<JSONObject> listOfJSONAppointment = new ArrayList<>();

			for (Appointment appointment : getAppointments(startDate, endDate, onBehafOf)) {
				listOfJSONAppointment.add(ToolBox.appointmentToJSON(appointment));
			}
			if (!listOfJSONAppointment.isEmpty())
				json.put(onBehafOf, listOfJSONAppointment);
		}

		return json;
	}

	public boolean cancelAppointment(Date startDate, Date endDate, String roomName) {
		try {
			FindItemsResults<Appointment> appointments = this.getAppointments(startDate, endDate, roomName);
			for (Appointment appt : appointments.getItems()) {
				appt.cancelMeeting();
				break;
			}
			return true;
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}

	public boolean declineMyAppointments(Date startDate, Date endDate) {
		try {

			this.decline(this.getAppointments(startDate, endDate, ConfigManager.getUsername()));
			return true;

		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}

	public boolean declineAppointmentsOnBehalfOf(Date startDate, Date endDate, String onBehafOf) {
		try {

			this.decline(this.getAppointments(startDate, endDate, onBehafOf));
			return true;

		} catch (Exception e) {
			e.printStackTrace();
			return false;
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
