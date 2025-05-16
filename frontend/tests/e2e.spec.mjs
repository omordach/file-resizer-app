import { test, expect } from '@playwright/test';
import path from 'path';

test('User can upload file, fill form, and process file', async ({ page }) => {
  // Open the application
  await page.goto('http://localhost:8000');

  // Upload file using hidden file input
  const filePath = path.resolve('tests/test-image.png'); // Make sure this file exists
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles(filePath);

  // Open the File Type dropdown
  await page.getByText('File Type').click();

  // Select 'Image' option safely without conflict
  await page.locator('div[role="option"]', { hasText: 'Image' }).click();

  // Fill width and height
  await page.locator('input#width').fill('300');
  await page.locator('input#height').fill('300');

  // Bypass reCAPTCHA or assume it's disabled in test mode
  // No action needed if DISABLE_CAPTCHA=true on backend

  // Submit the form
  const submitButton = page.getByRole('button', { name: /Process/ });
  await submitButton.click();

  // Expect success message
  await expect(page.locator('text=File processed successfully')).toBeVisible({ timeout: 10000 });
});
