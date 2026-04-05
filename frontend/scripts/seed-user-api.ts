/**
 * @fileoverview Seed script to create a test user using better-auth API.
 * This ensures that hashing and internal database state are handled correctly.
 */

import { auth } from "../src/lib/auth";

async function seed() {
  console.log("Seeding test user using Better Auth API...");
  
  const testEmail = "admin@precognito.ai";
  const testPassword = "Password123!";
  const userName = "Admin User";
  
  try {
    // Attempt to sign up
    // @ts-ignore
    const user = await auth.api.signUpEmail({
      body: {
        email: testEmail,
        password: testPassword,
        name: userName,
        role: "ADMIN", // Custom field we defined
      }
    });
    
    console.log("Test user created successfully!");
    console.log(`  Email: ${testEmail}`);
    console.log(`  Password: ${testPassword}`);
    console.log(`  Role: ADMIN`);
  } catch (err: any) {
    if (err.message?.includes("User already exists")) {
       console.log("User already exists, update role to ADMIN if needed.");
       // In a real script, we could update the role here if we wanted.
    } else {
       console.error("Error seeding user:", err);
    }
  } finally {
    process.exit(0);
  }
}

seed();
