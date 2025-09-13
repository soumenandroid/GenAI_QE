package com.genaiqe.module1;

import com.google.gson.Gson;
import org.openqa.selenium.*;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

public class SelfHealClient {

    static class HealPayload {
        String locatorKey;
        String original_locator;
        String html_snippet;

        HealPayload(String locatorKey, String original_locator, String html_snippet) {
            this.locatorKey = locatorKey;
            this.original_locator = original_locator;
            this.html_snippet = html_snippet;
        }
    }

    public static By resolve(WebDriver driver, By original, String locatorKey) {
        try {
            driver.findElement(original);
            return original;
        } catch (NoSuchElementException e) {
            try {
                // WebElement body = driver.findElement(By.tagName("body"));
                String html = driver.getPageSource();
                if (html.length() > 5000) {
                    html = html.substring(0, 5000); // still trim if too large
                    System.out.println("****************" + html);
                }
                System.out.println("****OUTSIDE************" + html);
                HealPayload payload = new HealPayload(locatorKey, original.toString(), html);
                Gson gson = new Gson();
                String json = gson.toJson(payload);

                URL url = new URL("http://127.0.0.1:8000/selfheal");
                HttpURLConnection con = (HttpURLConnection) url.openConnection();
                con.setRequestMethod("POST");
                con.setRequestProperty("Content-Type", "application/json");
                con.setDoOutput(true);

                try (OutputStream os = con.getOutputStream()) {
                    os.write(json.getBytes("utf-8"));
                }

                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = in.readLine()) != null) {
                    response.append(line);
                }
                in.close();

                String resp = response.toString();
                System.out.println("****** healed_locator******" + resp);
                if (resp.contains("healed_locator")) {
                    String selector = resp.replaceAll(".*\"healed_locator\"\\s*:\\s*\"([^\"]+)\".*", "$1");
                    selector = selector.trim();

                    // Decide if it's XPath or CSS
                    if (selector.startsWith("/") || selector.startsWith("(")) {
                        return By.xpath(selector);
                    } else {
                        return By.cssSelector(selector);
                    }
                }
            } catch (Exception ex) {
                ex.printStackTrace();
            }
            throw e;
        }
    }
}