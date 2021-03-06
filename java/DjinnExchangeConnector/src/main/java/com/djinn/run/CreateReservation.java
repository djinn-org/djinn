package com.djinn.run;

import com.djinn.ExchangeController;

public class CreateReservation {
	public static void main(String[] args) throws Exception {
		ExchangeController controler = ExchangeController.getInstanceOrDie();

		Arguments arguments = ArgumentParser.parseOrExit(args);

		boolean success = controler.makeAMeeting("", "", arguments.start, arguments.end, arguments.roomNames.get(0), "");

		controler.close();

		if (success) {
			System.out.println("OK");
		} else {
			System.out.println("failed");
			System.exit(1);
		}
	}
}
