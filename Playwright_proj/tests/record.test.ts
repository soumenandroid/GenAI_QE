import test, { expect } from "@playwright/test";

test('codegen login test', async ({ page }) => {
    await page.goto('https://ecommerce-playground.lambdatest.io/');
    await page.hover("//a[@data-toggle='dropdown']//span[contains(.,'My account')]")
    await page.getByRole('link', { name: 'Login' }).click();
    await page.getByRole('textbox', { name: 'E-Mail Address' }).click();
    await page.getByRole('textbox', { name: 'E-Mail Address' }).fill('coolcse49@gmail.com');
    await page.getByRole('textbox', { name: 'E-Mail Address' }).press('Tab');
    await page.getByRole('textbox', { name: 'Password' }).fill('Welcome#123');
    await page.getByRole('button', { name: 'Login' }).click();
    await expect(page.locator('#content')).toContainText('My Account');
    await page.getByRole('button', { name: ' My account' }).click();
    await page.getByRole('link', { name: ' Logout' }).click();
    await expect(page.locator('h1')).toContainText('Account Logout');
});