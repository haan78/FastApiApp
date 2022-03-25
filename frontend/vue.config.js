
module.exports = {

  pages: {
    "main":{ "entry":"./src/main.js", "template":"./main.html" }
  },

  filenameHashing: false,
  outputDir:"./static/dist",
  // delete HTML related webpack plugins
  chainWebpack: config => {
    config.plugins.delete('html')
    config.plugins.delete('preload')
    config.plugins.delete('prefetch')
  }
}