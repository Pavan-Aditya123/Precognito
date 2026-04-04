# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: inventory.spec.ts >> Inventory and Alerts >> should show alerts page
- Location: tests/e2e/inventory.spec.ts:17:2

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: locator('h1')
Expected substring: "Alerts"
Received string:    "Precognito"
Timeout: 5000ms

Call log:
  - Expect "to.have.text" with timeout 5000ms
  - waiting for locator('h1')
    9 × locator resolved to <h1 class="text-2xl font-bold text-[#f1f5f9]">Precognito</h1>
      - unexpected value "Precognito"

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e3]:
    - generic [ref=e4]:
      - link "Precognito" [ref=e5] [cursor=pointer]:
        - /url: /
        - heading "Precognito" [level=1] [ref=e6]
      - paragraph [ref=e7]: Sign in or create account
    - generic [ref=e9]:
      - generic [ref=e10]:
        - generic [ref=e11]: Email
        - textbox "Email" [ref=e12]:
          - /placeholder: Enter your email
      - generic [ref=e13]:
        - generic [ref=e14]: Password
        - textbox "Password" [ref=e15]:
          - /placeholder: Enter your password (min 8 chars)
      - button "Sign In / Register" [ref=e16]
    - paragraph [ref=e17]:
      - link "← Back to Home" [ref=e18] [cursor=pointer]:
        - /url: /
  - button "Open Next.js Dev Tools" [ref=e24] [cursor=pointer]:
    - generic [ref=e27]:
      - text: Compiling
      - generic [ref=e28]:
        - generic [ref=e29]: .
        - generic [ref=e30]: .
        - generic [ref=e31]: .
  - alert [ref=e32]
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
  13 |     await expect(page.locator("h1")).toContainText("Inventory");
  14 |     await expect(page.locator("text=JIT Alerts")).toBeVisible();
  15 |   });
  16 | 
  17 |   test("should show alerts page", async ({ page }) => {
  18 |     await page.goto("/alerts");
> 19 |     await expect(page.locator("h1")).toContainText("Alerts");
     |                                     ^ Error: expect(locator).toContainText(expected) failed
  20 |   });
  21 | });
  22 | 
```