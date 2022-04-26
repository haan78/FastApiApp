
const pages = {
  "main": { "entry": "./src/main.js" },
  "load":{ "entry": "./src/load.js" }
};

module.exports = {

  pages: pages,

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
    Object.keys(pages).forEach(page => {
      config.plugins.delete(`html-${page}`);
      config.plugins.delete(`preload-${page}`);
      config.plugins.delete(`prefetch-${page}`);
    });
  }
};