# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: reports.spec.ts >> Reports and Analytics >> should display analytics page
- Location: tests/e2e/reports.spec.ts:17:2

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: goto: net::ERR_ABORTED; maybe frame was detached?
Call log:
  - navigating to "http://localhost:3000/analytics", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from "@playwright/test";
  2  | 
  3  | test.describe("Reports and Analytics", () => {
  4  |   test.beforeEach(async ({ page }) => {
  5  |     await page.goto("/login");
  6  |     await page.fill('input[type="email"]', "admin@precognito.ai");
  7  |     await page.fill('input[type="password"]', "Password123!");
  8  |     await page.click('button[type="submit"]');
  9  |   });
  10 | 
  11 |   test("should display reporting page with export options", async ({ page }) => {
  12 |     await page.goto("/reports");
  13 |     await expect(page.locator("h1")).toContainText("Reports");
  14 |     await expect(page.locator("text=Export PDF")).toBeVisible();
  15 |   });
  16 | 
  17 |   test("should display analytics page", async ({ page }) => {
> 18 |     await page.goto("/analytics");
     |               ^ Error: goto: net::ERR_ABORTED; maybe frame was detached?
  19 |     await expect(page.locator("h1")).toContainText("Analytics");
  20 |     await expect(page.locator("text=Precision")).toBeVisible();
  21 |   });
  22 | });
  23 | 
```