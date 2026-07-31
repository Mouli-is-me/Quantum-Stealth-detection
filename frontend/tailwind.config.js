/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'c2-bg': 'var(--bg-base)',
        'c2-panel': 'var(--panel-bg)',
        'c2-border': 'var(--panel-border)',
        'c2-text-main': 'var(--text-primary)',
        'c2-text-sub': 'var(--text-secondary)',
        'c2-green': 'var(--color-primary)',
        'c2-green-bright': 'var(--color-primary-bright)',
        'c2-cyan': 'var(--color-secondary)',
        'c2-amber': 'var(--color-warning)',
        'c2-red': 'var(--color-critical)',
        'c2-grey': 'var(--color-offline)',
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', '"IBM Plex Mono"', 'monospace'],
        sans: ['"IBM Plex Sans"', 'Inter', 'sans-serif'],
      },
      borderRadius: {
        'none': '0px',
        'sm': '2px',
        'DEFAULT': '2px',
      },
      animation: {
        'radar-sweep': 'sweep 4s linear infinite',
        'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'led-glow': 'ledGlow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        sweep: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        ledGlow: {
          '0%': { opacity: '0.6' },
          '100%': { opacity: '1' },
        }
      }
    },
  },
  plugins: [],
};
