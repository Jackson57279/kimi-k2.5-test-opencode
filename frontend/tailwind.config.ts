import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      // Railway Design System Colors
      colors: {
        // Base semantic colors (CSS variables)
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        // Railway accent colors
        railway: {
          bg: "#020617",
          card: "#111827",
          indigo: "#4f46e5",
          violet: "#7c3aed",
          cyan: "#22d3ee",
          purple: "#a855f7",
          green: "#22c55e",
          red: "#ef4444",
          amber: "#f59e0b",
        },
      },
      // Custom fonts for Railway UI
      fontFamily: {
        sans: ["Inter", "Geist", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      // Border radius
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      // Railway animations
      keyframes: {
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        "fade-out": {
          "0%": { opacity: "1" },
          "100%": { opacity: "0" },
        },
        "slide-in-up": {
          "0%": { transform: "translateY(10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        "slide-in-down": {
          "0%": { transform: "translateY(-10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        "slide-in-left": {
          "0%": { transform: "translateX(-10px)", opacity: "0" },
          "100%": { transform: "translateX(0)", opacity: "1" },
        },
        "slide-in-right": {
          "0%": { transform: "translateX(10px)", opacity: "0" },
          "100%": { transform: "translateX(0)", opacity: "1" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        pulse: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
        glow: {
          "0%, 100%": { boxShadow: "0 0 5px rgba(79, 70, 229, 0.5)" },
          "50%": { boxShadow: "0 0 20px rgba(79, 70, 229, 0.8), 0 0 30px rgba(124, 58, 237, 0.4)" },
        },
        "terminal-blink": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0" },
        },
        "gradient-shift": {
          "0%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
          "100%": { backgroundPosition: "0% 50%" },
        },
      },
      animation: {
        "fade-in": "fade-in 0.2s ease-out",
        "fade-out": "fade-out 0.2s ease-out",
        "slide-in-up": "slide-in-up 0.3s ease-out",
        "slide-in-down": "slide-in-down 0.3s ease-out",
        "slide-in-left": "slide-in-left 0.3s ease-out",
        "slide-in-right": "slide-in-right 0.3s ease-out",
        shimmer: "shimmer 2s linear infinite",
        pulse: "pulse 2s ease-in-out infinite",
        glow: "glow 2s ease-in-out infinite",
        "terminal-blink": "terminal-blink 1s step-end infinite",
        "gradient-shift": "gradient-shift 3s ease infinite",
      },
      // Glassmorphism backdrop blur values
      backdropBlur: {
        xs: "2px",
      },
      // Box shadow for glassmorphism and glow effects
      boxShadow: {
        glass: "0 8px 32px 0 rgba(0, 0, 0, 0.36)",
        "glass-sm": "0 4px 16px 0 rgba(0, 0, 0, 0.24)",
        "glow-indigo": "0 0 20px rgba(79, 70, 229, 0.5)",
        "glow-violet": "0 0 20px rgba(124, 58, 237, 0.5)",
        "glow-cyan": "0 0 20px rgba(34, 211, 238, 0.5)",
      },
      // Background image for gradients
      backgroundImage: {
        "gradient-railway": "linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)",
        "gradient-railway-hover": "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
        "gradient-glow": "radial-gradient(ellipse at center, rgba(79, 70, 229, 0.15) 0%, transparent 70%)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

export default config
