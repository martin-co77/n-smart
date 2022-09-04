/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      maxWidth: {
        '1440': '1440px'
      },
      spacing: {

      },
      fontFamily: {
        'roboto': 'Roboto'
      },
      boxShadow: {
        'button': '2px 2px 2px 1px rgba(0, 0, 0, 0.25)',
      }
    },
  },
  plugins: [],
}
