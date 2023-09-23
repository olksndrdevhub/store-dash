/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./templates/**/*.{html,js}",
      "./**/templates/**/*.{html,js}"
    ],
    theme: {
      colors: {
        // Using modern `rgb`
        primary: 'rgb(var(--color-primary) / <alpha-value>)',
        secondary: 'rgb(var(--color-secondary) / <alpha-value>)',
        'active-dimmed': 'rgb(var(--color-active-dimmed) / <alpha-value>)',
        accent: 'rgb(var(--color-accent) / <alpha-value>)',
        'accent-secondary': 'rgb(var(--color-accent-secondary) / <alpha-value>)',
        'action-success': 'rgb(var(--color-action-success) / <alpha-value>)',
        'action-danger': 'rgb(var(--color-action-danger) / <alpha-value>)',
        'text-primary': 'rgb(var(--color-text-primary) / <alpha-value>)',
        'text-dimmed': 'rgb(var(--color-text-dimmed) / <alpha-value>)',
        'text-minor': 'rgb(var(--color-text-minor) / <alpha-value>)',
      },
      extend: {},
    },
    plugins: [],
  }