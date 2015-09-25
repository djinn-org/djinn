package com.djinn.run;

import com.djinn.ExchangeController;

public class ListReservations {

	public static void main(String[] args) throws Exception {
		ExchangeController controler = ExchangeController.getInstanceOrDie();

		Arguments arguments = ArgumentParser.parseOrExit(args);

		String json =
				controler.findManyUserAppointments(arguments.start, arguments.end, arguments.roomNames);

		System.out.println(json);

		controler.close();
	}
}
