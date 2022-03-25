
module.exports = {

  pages: {
    "main":{ "entry":"./js/main.js", "template":"./main.html" }
  },

  filenameHashing: false,
  outputDir:"./static",
  // delete HTML related webpack plugins
  chainWebpack: config => {
    config.plugins.delete('html')
    config.plugins.delete('preload')
    config.plugins.delete('prefetch')
  }
}