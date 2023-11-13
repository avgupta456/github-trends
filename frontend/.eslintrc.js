module.exports = {
  env: {
    browser: true,
    es6: true,
  },
  extends: ['airbnb', 'plugin:prettier/recommended'],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  plugins: ['react', 'prettier'],
  rules: {
    'react/jsx-filename-extension': 'off',
    'react/forbid-prop-types': 'off',
    'react/destructuring-assignment': 'off',
    'import/prefer-default-export': 'off',
    'react/function-component-definition': 'off',
    'react/no-unstable-nested-components': 'off',
    'jsx-a11y/control-has-associated-label': 'off',
    'no-console': 'off',
    radix: 'off',
    'prettier/prettier': [
      'error',
      {
        endOfLine: 'auto',
      },
    ],
  },
};
