import { test, expect } from '@playwright/test';
import path from 'path';

test('User can upload file, fill form, and process file', async ({ page }) => {
  await page.goto('/');

  // Locate dropzone and upload file
const filePath = path.resolve('tests/test-image.png'); // Ensure this file exists
const fileInput = page.locator('input[type="file"]');
await fileInput.setInputFiles(filePath);

  // Select Image type
  await page.getByText('File Type').click();
  await page.locator('div[role="option"]', { hasText: 'Image' }).click();

  // Fill width and height
  await page.locator('input#width').fill('300');
  await page.locator('input#height').fill('300');

  // Complete dummy reCAPTCHA if skipped in test mode, otherwise simulate
  // Skipped for now as reCAPTCHA blocks automation.

  // Click Process button
  const button = page.getByRole('button', { name: /Process/ });
  await button.click();

  // Expect message about success or error
  await expect(page.locator('text=File processed successfully')).toBeVisible({ timeout: 10000 });
});
