package com.djinn.run;

import java.util.Date;
import java.util.List;

public class Arguments {

	public final Date start;
	public final Date end;
	public final List<String> roomNames;

	public Arguments(Date start, Date end, List<String> roomNames) {
		this.start = start;
		this.end = end;
		this.roomNames = roomNames;
	}
}
