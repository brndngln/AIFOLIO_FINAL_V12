import react from "eslint-plugin-react";
import tsPlugin from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";

export default [
  {
    files: ["**/*.{js,jsx,ts,tsx}", "*.js", "*.jsx", "*.ts", "*.tsx"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      parser: tsParser,
    },
    plugins: {
      react,
      "@typescript-eslint": tsPlugin,
    },
    settings: {
      react: { version: "detect" },
    },
    rules: {
      "no-unused-vars": "warn",
      "no-console": "off",
      "react/prop-types": "off",
      "react/react-in-jsx-scope": "off",
    },
  },
  {
    plugins: {
      react,
      "@typescript-eslint": tsPlugin,
    },
    languageOptions: {
      parser: tsParser,
    },
    settings: {
      react: { version: "detect" },
    },
    rules: {
      "react/prop-types": "off",
      "react/react-in-jsx-scope": "off",
    },
  },
];
