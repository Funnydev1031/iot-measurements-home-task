/** @format */

module.exports = (api) => {
  api.cache(true);

  return {
    presets: ['react-app'],
    plugins: [
      'babel-plugin-styled-components',
      ['@babel/plugin-transform-react-jsx'],
      ['module-resolver', { root: ['.'] }],
      ["@babel/plugin-proposal-private-property-in-object", { "loose": true }],
      ["@babel/plugin-proposal-private-methods", { "loose": true }],
      ["@babel/plugin-proposal-class-properties", { "loose": true }]
    ],
  };
};
