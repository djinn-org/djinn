package com.djinn;

import java.net.URI;
import java.net.URISyntaxException;
import java.text.ParseException;
import java.util.Date;

import microsoft.exchange.webservices.data.core.ExchangeService;
import microsoft.exchange.webservices.data.core.enumeration.property.WellKnownFolderName;
import microsoft.exchange.webservices.data.core.service.folder.CalendarFolder;
import microsoft.exchange.webservices.data.core.service.item.Appointment;
import microsoft.exchange.webservices.data.core.service.item.EmailMessage;
import microsoft.exchange.webservices.data.credential.ExchangeCredentials;
import microsoft.exchange.webservices.data.credential.WebCredentials;
import microsoft.exchange.webservices.data.property.complex.FolderId;
import microsoft.exchange.webservices.data.property.complex.Mailbox;
import microsoft.exchange.webservices.data.search.CalendarView;

public class ConnectionManager {

	//Singleton
	private static ConnectionManager instance = null;

	//CONSTANTS
	public static String dateFormat = "yyyy-MM-dd HH:mm:ss";

	//EWS API service
	private ExchangeService service = null;

	//Constructor
	private ConnectionManager() throws Exception {
		this.service = new ExchangeService();
		ExchangeCredentials credentials =
				new WebCredentials(ConfigManager.getUsername(), ConfigManager.getPassword(), ConfigManager.getDomain());
		service.setCredentials(credentials);

		try {
			service.setUrl(new URI(ConfigManager.getWebServiceUrl()));
		} catch (URISyntaxException e) {
			e.printStackTrace();
			throw new Exception("Something wrong with the url", e);
		}
	}

	//

	/**
	 * Singleton getInstance
	 *
	 * @return
	 * @throws Exception if something went wrong on the API service instantiation
	 */
	public static ConnectionManager getInstance() throws Exception {
		if (instance == null)
			instance = new ConnectionManager();

		return instance;
	}

	/**
	 * Gives you a new email to fill and send
	 *
	 * @return
	 * @throws Exception
	 */
	public EmailMessage getNewEmail() throws Exception {
		return new EmailMessage(service);
	}

	/**
	 * Gives you a new appointment to fill and send
	 *
	 * @return
	 * @throws Exception
	 */
	public Appointment getNewappointment() throws Exception {
		return new Appointment(service);
	}

	public CalendarFolder getMyCalendar() throws Exception {
		return CalendarFolder.bind(service, WellKnownFolderName.Calendar);
	}

	public CalendarFolder getSomeoneCalendar(String someone) throws Exception {
		return CalendarFolder.bind(service, getSomeoneFolderId(someone));
	}

	public FolderId getSomeoneFolderId(String someone) {
		return new FolderId(
				WellKnownFolderName.Calendar,
				new Mailbox(someone + "@" + ConfigManager.getMailDomain()));
	}

	public CalendarView getNewCalendarView(String startDate, String endDate) throws ParseException {
		Date startDat = ToolBox.formatDate(startDate);
		Date endDat = ToolBox.formatDate(endDate);

		return new CalendarView(startDat, endDat);
	}

	public void close() {
		this.service.close();
	}

}
