import { chromium, expect } from "@playwright/test"
import { ai } from '@zerostep/playwright'
import { test } from './test-with-fixture.ts'

test.describe('SauceDemo', () => {
    test.setTimeout(150_000)
    test('codegen login test', async ({ page, ai }) => {
        await page.goto('https://ecommerce-playground.lambdatest.io/');
        await page.hover("//a[@data-toggle='dropdown']//span[contains(.,'My account')]")
        await page.click("'Register'")
        await page.waitForTimeout(2000)

        await ai('Enter First Name = ABC , Last Name = XYZ, Email address = coolcse49@gmail.com, Telephone = 9876563459 and password as Welcome#123')
        await ai('Confirm I have read and agree to the Privacy Policy')
        await ai('Click on Continue')

        await page.waitForTimeout(5000)

    })
})