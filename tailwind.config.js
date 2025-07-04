/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/8**/*.html",   //template for project level
    "./**/templates/**/*.html", //templates inside apps

  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

