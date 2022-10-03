/* eslint-disable global-require */
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    screens: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px',
      '3xl': '1792px',
    },
    extend: {
      fontFamily: {
        typist: ['Playfair Display SC', 'Courier New'],
      },
    },
  },
  plugins: [require('daisyui')],
};
