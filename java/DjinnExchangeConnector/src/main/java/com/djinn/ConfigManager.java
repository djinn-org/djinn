package com.djinn;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class ConfigManager {

	private static final Properties properties = new Properties();

	static {
		try (InputStream stream = ConfigManager.class.getResourceAsStream("/config.properties")) {
			properties.load(stream);
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(1);
		}
	}

	private ConfigManager() {
		throw new AssertionError("Utility class, forbidden constructor");
	}

	public static String getMailDomain() {
		return properties.getProperty("mail.domain");
	}

	public static String getDomain() {
		return properties.getProperty("domain");
	}

	public static String getUsername() {
		return properties.getProperty("username");
	}

	public static String getPassword() {
		return properties.getProperty("password");
	}

	public static String getWebServiceUrl() {
		return properties.getProperty("ws.url");
	}
}
