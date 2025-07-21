// AIFOLIO Elite System - Babel Configuration
// Optimized for testing, TypeScript, and development

module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        targets: {
          node: 'current',
        },
        modules: 'auto'
      }
    ],
    [
      '@babel/preset-react',
      {
        runtime: 'automatic',
        development: process.env.NODE_ENV === 'development'
      }
    ],
    '@babel/preset-typescript'
  ],

  env: {
    test: {
      presets: [
        [
          '@babel/preset-env',
          {
            targets: {
              node: 'current'
            }
          }
        ],
        '@babel/preset-react',
        '@babel/preset-typescript'
      ]
    }
  }
};
