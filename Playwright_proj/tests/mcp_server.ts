import { test, expect } from '@playwright/test';

test('Navigate to Nasdaq and search for Apple stock symbol', async ({ page }) => {
  // Navigate to the Nasdaq website
  await page.goto('https://www.nasdaq.com/');

  // Locate the search input and type "Apple"
  const searchInput = page.locator('input[placeholder="Search for a Symbol"]');
  await searchInput.fill('Apple');
  await searchInput.press('Enter');

  // Wait for the search results page to load
  await page.waitForURL('**/search?q=Apple**');

  // Validate that the Apple stock symbol (AAPL) appears in the results
  const appleStockLink = page.locator('a:has-text("Apple Inc. Common Stock (AAPL)")');
  await expect(appleStockLink).toBeVisible();

  // Optionally, click on the link to navigate to the stock details page
  await appleStockLink.click();

});