package com.djinn.run;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class ArgumentParser {

	private static final DateFormat dateFormat = new SimpleDateFormat("yyyyMMddHHmm");

	static class NotEnoughArgumentsException extends Exception {}

	static class InvalidDateValuesException extends Exception {}

	public static Arguments parse(String[] args) throws NotEnoughArgumentsException, ParseException, InvalidDateValuesException {
		if (args.length < 3) {
			throw new NotEnoughArgumentsException();
		}

		Date start = parseDate(args[0]);
		Date end = parseDate(args[1]);
		if (start.equals(end) || start.after(end)) {
			throw new InvalidDateValuesException();
		}

		List<String> roomNames = new ArrayList<>();
		for (int i = 2; i < args.length; ++i) {
			roomNames.add(args[i].replaceAll("[.-]", ""));
		}
		return new Arguments(start, end, roomNames);
	}

	public static Arguments parseOrExit(String[] args) {
		try {
			return parse(args);
		} catch (NotEnoughArgumentsException e) {
			printError("Not enough arguments");
		} catch (ParseException e) {
			printError("Invalid date format");
		} catch (InvalidDateValuesException e) {
			printError("Invalid date values (same or wrong order)");
		}
		printUsage(1);
		throw new AssertionError("Unreachable statement");
	}

	private static Date parseDate(String datestr) throws ParseException {
		return dateFormat.parse(datestr);
	}

	private static void printError(String message) {
		System.err.println("Fatal: " + message);
	}

	private static void printUsage(int exitCode) {
		System.out.println("usage: java %prog START END ROOM");
		System.out.println("Date format: YYYYMMDDHHmm");
		System.exit(exitCode);
	}
}
