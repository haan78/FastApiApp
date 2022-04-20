
//const defineConfig = require('@vue/cli-service')

module.exports = {

  pages: {
    "main": { "entry": "./src/main.js", "template": "./main.html" }
  },

  filenameHashing: false,
  outputDir: "/static/dist",
  productionSourceMap:true,
  css: {
    extract: true
  },
  // delete HTML related webpack plugins
  configureWebpack: (config) => {
    config.watchOptions = { /*WSL Volume problem*/
      poll: 1000,
      ignored: /node_modules/
    };

  },



  chainWebpack: config => {
    config.devtool = 'source-map';
    config.plugins.delete('html');
    config.plugins.delete('preload');
    config.plugins.delete('prefetch');
  }
};