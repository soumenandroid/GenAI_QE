import { chromium, expect } from "@playwright/test"
import { ai } from '@zerostep/playwright'
import { test } from './test-with-fixture.ts'

test.describe('SauceDemo', () => {
    test('can login and logout', async ({ page, ai }) => {
        await page.goto('https://www.saucedemo.com/')
        const [username, password] = await ai([
            'Get the first accepted username',
            'Get the accepted password',
        ])
        await ai([
            `Enter ${username} as the username`,
            `Enter ${password} as the password`
        ])
        await ai('Click Login')
        await ai('Click the menu button')
        await ai('Click the logout link')
    })

    test('codegen login test', async ({ page, ai }) => {
        await page.goto('https://ecommerce-playground.lambdatest.io/');
        await page.hover("//a[@data-toggle='dropdown']//span[contains(.,'My account')]")
        await ai('Goto Log in page')

        await ai('Log in with email address coolcse49@gmail.com and password Welcome#123')
    })
})