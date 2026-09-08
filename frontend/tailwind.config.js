/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#0B132B',
          800: '#1C2541',
          700: '#3A506B',
          600: '#486581',
        },
        accent: {
          cyan: '#00B4D8',
          blue: '#0077B6',
          emerald: '#10B981',
          amber: '#F59E0B',
          rose: '#EF4444',
        }
      }
    },
  },
  plugins: [],
}