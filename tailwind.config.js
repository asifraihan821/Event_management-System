/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",   //template for project level
    "./**/templates/**/*.html", //templates inside apps

  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

