# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: dashboard.spec.ts >> Dashboard Functionality >> should display welcome message and status cards
- Location: tests/e2e/dashboard.spec.ts:13:2

# Error details

```
Error: expect(page).toHaveURL(expected) failed

Expected pattern: /.*dashboard/
Received string:  "http://localhost:3000/login?"
Timeout: 5000ms

Call log:
  - Expect "to.have.url" with timeout 5000ms
    9 × unexpected value "http://localhost:3000/login?"

```

# Page snapshot

```yaml
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
```

# Test source

```ts
  1  | import { test, expect } from "@playwright/test";
  2  | 
  3  | test.describe("Dashboard Functionality", () => {
  4  |   test.beforeEach(async ({ page }) => {
  5  |     // In a real E2E environment, we would use global setup to handle authentication once
  6  |     await page.goto("/login");
  7  |     await page.fill('input[type="email"]', "admin@precognito.ai");
  8  |     await page.fill('input[type="password"]', "Password123!");
  9  |     await page.click('button[type="submit"]');
> 10 |     await expect(page).toHaveURL(/.*dashboard/);
     |                       ^ Error: expect(page).toHaveURL(expected) failed
  11 |   });
  12 | 
  13 |   test("should display welcome message and status cards", async ({ page }) => {
  14 |     await expect(page.locator("h1")).toContainText("Welcome back");
  15 |     await expect(page.locator("text=Total Assets")).toBeVisible();
  16 |     await expect(page.locator("text=Healthy")).toBeVisible();
  17 |   });
  18 | 
  19 |   test("should navigate to assets page from dashboard", async ({ page }) => {
  20 |     // Look for a link to assets or a card that navigates
  21 |     const assetsLink = page.locator('a[href="/assets"]');
  22 |     if (await assetsLink.count() > 0) {
  23 |         await assetsLink.first().click();
  24 |         await expect(page).toHaveURL(/.*assets/);
  25 |     }
  26 |   });
  27 | });
  28 | 
```