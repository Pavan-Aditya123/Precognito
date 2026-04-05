/**
 * @fileoverview Theme provider for managing Dark/Light modes.
 */

"use client";

import React, { createContext, useContext, useEffect, useState } from "react";

/** Supported theme modes. */
type Theme = "dark" | "light";

/** Context state for theme management. */
interface ThemeContextType {
  /** The current active theme. */
  theme: Theme;
  /** Function to switch between dark and light themes. */
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

/**
 * Provides theme state to its children.
 * 
 * @param {Object} props Component props.
 * @param {React.ReactNode} props.children The children to wrap.
 * @returns {JSX.Element} The theme provider component.
 */
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>("dark");

  useEffect(() => {
    const savedTheme = localStorage.getItem("precognito-theme") as Theme;
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.classList.toggle("light", savedTheme === "light");
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    localStorage.setItem("precognito-theme", newTheme);
    document.documentElement.classList.toggle("light", newTheme === "light");
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

/**
 * Hook to access the theme context.
 * 
 * @returns {ThemeContextType} The current theme and toggle function.
 * @throws {Error} If used outside of ThemeProvider.
 */
export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}
