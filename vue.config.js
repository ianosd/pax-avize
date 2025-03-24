module.exports = {
  pluginOptions: {
    electronBuilder: {
      preload: 'src/preload.js',
      // Or, for multiple preload files:
      preload: { preload: 'src/preload.js' },
        apId: 'ianosd.electric-paper',
        win: {
          target: ["portable"]
        }
    }
  }
}