import test, { chromium, expect } from "@playwright/test"

test('Search test', async () => {

    const browser = await chromium.launch({
        headless: false
    })

    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto("https://playwright.dev/")
    await page.click("//span[contains(text(),'Search')]")
    await page.fill("//input[@id='docsearch-input']", "Install")
    await page.keyboard.press('Enter')
    await page.waitForTimeout(5000)

});

test('Login test', async () => {
    test.setTimeout(150_000)

    const browser = await chromium.launch({
        headless: false
    })

    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto("https://ecommerce-playground.lambdatest.io/")
    await page.hover("//a[@data-toggle='dropdown']//span[contains(.,'My account')]")
    await page.click("'Login'")
    await page.fill("//input[@id='input-email']", "coolcse49@gmail.com")
    await page.fill("//input[@id='input-password']", "Welcome#123")
    await page.click("input[value='Login']")
    await page.waitForTimeout(5000)

    const newPage = await context.newPage()
    await newPage.goto("https://ecommerce-playground.lambdatest.io/")
    await page.waitForTimeout(5000)

    const newContext = await browser.newContext()
    const newPage1 = await newContext.newPage()
    await newPage1.goto("https://ecommerce-playground.lambdatest.io/")
    await page.waitForTimeout(5000)

})

