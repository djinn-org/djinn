package com.djinn.run;

import java.text.ParseException;
import java.util.Arrays;
import java.util.Collections;

import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class ArgumentParserTest {
	@Test(expected = ArgumentParser.NotEnoughArgumentsException.class)
	public void fails_if_no_args() throws Exception {
		ArgumentParser.parse(new String[]{});
	}

	@Test(expected = ArgumentParser.NotEnoughArgumentsException.class)
	public void fails_if_not_enough_args() throws Exception {
		ArgumentParser.parse(new String[]{"a", "b"});
	}

	@Test(expected = ParseException.class)
	public void fails_if_invalid_dates() throws Exception {
		ArgumentParser.parse(new String[]{"201509251351", "x", "room"});
	}

	@Test(expected = ArgumentParser.InvalidDateValuesException.class)
	public void fails_if_unordered_dates() throws Exception {
		ArgumentParser.parse(new String[]{"201509251351", "201509251350", "room"});
	}

	@Test(expected = ArgumentParser.InvalidDateValuesException.class)
	public void fails_if_same_dates() throws Exception {
		ArgumentParser.parse(new String[]{"201509251351", "201509251351", "room"});
	}

	@Test
	public void ok_with_one_room() throws Exception {
		Arguments args = ArgumentParser.parse(new String[]{"201509251351", "201509251352", "room"});
		assertEquals(Collections.singletonList("room"), args.roomNames);
	}

	@Test
	public void ok_with_two_rooms() throws Exception {
		Arguments args = ArgumentParser.parse(new String[]{"201509251351", "201509251352", "room1", "room2"});
		assertEquals(Arrays.asList("room1", "room2"), args.roomNames);
	}

	@Test
	public void simplified_room_name() throws Exception {
		Arguments args = ArgumentParser.parse(new String[]{"201509251351", "201509251352", "room1", "91A-12.J54"});
		assertEquals(Arrays.asList("room1", "91A12J54"), args.roomNames);
	}
}