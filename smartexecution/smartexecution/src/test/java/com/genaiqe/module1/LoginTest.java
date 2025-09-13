package com.genaiqe.module1;

import org.openqa.selenium.By;
import org.testng.annotations.Test;

public class LoginTest extends BaseTest {
    @Test
    public void testLogin() throws InterruptedException {
        driver.findElement(SelfHealClient.resolve(driver, By.id("user_name"), "username")).sendKeys("user1");
        Thread.sleep(1000);
        driver.findElement(SelfHealClient.resolve(driver, By.id("password_login"), "password"))
                .sendKeys("pass1");
        Thread.sleep(10000);
        driver.findElement(SelfHealClient.resolve(driver, By.id("login-btn"), "loginBtn")).click();
    }
}
