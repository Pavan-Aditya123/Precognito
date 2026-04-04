# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: inventory.spec.ts >> Inventory and Alerts >> should display inventory management page
- Location: tests/e2e/inventory.spec.ts:11:2

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: expect(locator).toContainText(expected) failed

Locator: locator('h1')
Expected substring: "Inventory"
Error: element(s) not found

Call log:
  - Expect "to.have.text" with timeout 5000ms
  - waiting for locator('h1')

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e3]: Loading session...
  - button "Open Next.js Dev Tools" [ref=e9] [cursor=pointer]:
    - generic [ref=e12]:
      - text: Compiling
      - generic [ref=e13]:
        - generic [ref=e14]: .
        - generic [ref=e15]: .
        - generic [ref=e16]: .
  - alert [ref=e17]
```

# Test source

```ts
  1  | import { test, expect } from "@playwright/test";
  2  | 
  3  | test.describe("Inventory and Alerts", () => {
  4  |   test.beforeEach(async ({ page }) => {
  5  |     await page.goto("/login");
  6  |     await page.fill('input[type="email"]', "admin@precognito.ai");
  7  |     await page.fill('input[type="password"]', "Password123!");
  8  |     await page.click('button[type="submit"]');
  9  |   });
  10 | 
  11 |   test("should display inventory management page", async ({ page }) => {
  12 |     await page.goto("/inventory");
> 13 |     await expect(page.locator("h1")).toContainText("Inventory");
     |                                     ^ Error: expect(locator).toContainText(expected) failed
  14 |     await expect(page.locator("text=JIT Alerts")).toBeVisible();
  15 |   });
  16 | 
  17 |   test("should show alerts page", async ({ page }) => {
  18 |     await page.goto("/alerts");
  19 |     await expect(page.locator("h1")).toContainText("Alerts");
  20 |   });
  21 | });
  22 | 
```