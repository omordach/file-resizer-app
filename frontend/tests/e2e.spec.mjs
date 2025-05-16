import { test, expect } from '@playwright/test';

test('Page loads and shows upload button', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('text=File Upload')).toBeVisible();
});
