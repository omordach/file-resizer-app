import { test, expect } from '@playwright/test';
import path from 'path';

test('Page loads and all key elements are visible', async ({ page }) => {
  await page.goto('/');

  // Check for page title
  await expect(page.locator('text=Resize File')).toBeVisible();

  // Check for drag & drop area or file input
  await expect(page.locator('input[type="file"]')).toBeVisible();

  // Check for File Type select trigger
  await expect(page.getByText('File Type')).toBeVisible();

  // Check for reCAPTCHA frame or placeholder (optional check)
  await expect(page.locator('iframe')).toBeVisible();

  // Check for Process button
  await expect(page.getByRole('button', { name: /Process/ })).toBeVisible();
});
