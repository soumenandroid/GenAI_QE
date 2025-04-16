import { test, expect } from '@playwright/test';

test('Search for flight from CCU to London on MakeMyTrip', async ({ page }) => {
  // Navigate to MakeMyTrip
  await page.goto('https://www.makemytrip.com');

  // Close any pop-ups or modals
  await page.click('body'); // Click on the body to close pop-ups

  // Select the "From" city
  await page.click('#fromCity');
  await page.fill('input[placeholder="From"]', 'CCU');
  await page.waitForSelector('li[role="option"]');
  await page.click('li[role="option"]:has-text("Kolkata")');

  // Select the "To" city
  await page.click('#toCity');
  await page.fill('input[placeholder="To"]', 'London');
  await page.waitForSelector('li[role="option"]');
  await page.click('li[role="option"]:has-text("London")');

  // Select the departure date (default is set to the nearest available date)
  await page.click('label[for="departure"]');
  await page.click('.DayPicker-Day--available');

  // Click on the search button
  await page.click('a[title="Search"]');

  // Wait for search results to load
  await page.waitForSelector('.listingCard');

  // Select the cheapest flight
  const prices = await page.$$eval('.listingCard .priceSection', elements => {
    return elements.map(el => {
      const priceText = el.textContent?.replace(/[^0-9]/g, '');
      return priceText ? parseInt(priceText, 10) : Infinity;
    });
  });

  const cheapestIndex = prices.indexOf(Math.min(...prices));
  const cheapestFlight = (await page.$$('.listingCard'))[cheapestIndex];
  await cheapestFlight?.click();

  // Add assertions if needed
  await expect(page).toHaveURL(/.*review/);
});