package com.genaiqe.module1;

import org.openqa.selenium.*;
import java.net.*;
import java.io.*;

public class SelfHealClient_module1 {
    public static By resolve(WebDriver driver, By original, String locatorKey) {
        try {
            driver.findElement(original);
            return original; // works fine
        } catch (NoSuchElementException e) {
            // Call FastAPI for healed locator
            try {
                URL url = new URL("http://localhost:8000/selfheal?locatorKey=" + locatorKey);
                HttpURLConnection con = (HttpURLConnection) url.openConnection();
                con.setRequestMethod("GET");

                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String response = in.readLine();
                in.close();

                // crude parse for demo
                String healed = response.replace("{\"healed_locator\":\"", "").replace("\"}", "");
                if (!healed.isEmpty()) {
                    return By.xpath(healed);
                }
            } catch (Exception ex) {
                ex.printStackTrace();
            }
            throw e;
        }
    }
}
