# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: work_orders.spec.ts >> Work Orders Flow >> should display work orders management
- Location: tests/e2e/work_orders.spec.ts:11:2

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: goto: net::ERR_ABORTED; maybe frame was detached?
Call log:
  - navigating to "http://localhost:3000/work-orders", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from "@playwright/test";
  2  | 
  3  | test.describe("Work Orders Flow", () => {
  4  |   test.beforeEach(async ({ page }) => {
  5  |     await page.goto("/login");
  6  |     await page.fill('input[type="email"]', "admin@precognito.ai");
  7  |     await page.fill('input[type="password"]', "Password123!");
  8  |     await page.click('button[type="submit"]');
  9  |   });
  10 | 
  11 |   test("should display work orders management", async ({ page }) => {
> 12 |     await page.goto("/work-orders");
     |               ^ Error: goto: net::ERR_ABORTED; maybe frame was detached?
  13 |     await expect(page.locator("h1")).toContainText("Work Orders");
  14 |     await expect(page.locator("text=Assigned To")).toBeVisible();
  15 |   });
  16 | });
  17 | 
```