const tsp = require('@typescript-eslint/eslint-plugin');
const tsa = require('@typescript-eslint/parser');

module.exports = [
    {
        files: ["js/*.ts"],
        rules: {
            semi: "error",
            "prefer-const": "error"
        },
        plugins: { '@typescript-eslint': tsp },
        languageOptions: {
            ecmaVersion: 2015,
            sourceType: "module",
            parser: tsa
        }
    }
];