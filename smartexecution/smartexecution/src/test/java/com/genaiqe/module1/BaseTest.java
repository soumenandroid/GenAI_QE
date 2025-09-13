package com.genaiqe.module1;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.*;

public class BaseTest {
    protected WebDriver driver;

    @BeforeClass
    public void setUp() {
        driver = new ChromeDriver();
        driver.manage().window().maximize();
        driver.get("http://127.0.0.1:3000/smartexecution/smartexecution/login.html"); // Demo login page
    }

    @AfterClass
    public void tearDown() {
        if (driver != null)
            driver.quit();
    }
}
