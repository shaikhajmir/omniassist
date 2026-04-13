/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0F172A', // deep space
        panel: '#1E293B',
        accent: '#38BDF8', // light blue
        critical: '#EF4444',
        warning: '#F59E0B',
        safe: '#10B981',
      }
    },
  },
  plugins: [],
}
