module.exports = {
  // it seems like the command npm run build:electron does not use this TODO
  pluginOptions: {
    electronBuilder: {
      preload: 'src/preload.js',
      // Or, for multiple preload files:
      preload: { preload: 'src/preload.js' },
      appId: 'ianosd.electric-paper',
      productName: 'Pax Avize', // Name of the app
      directories: {
        output: 'dist_electron' // Output directory for the build
      },
      win: {
        target: ["portable"] // Generate a portable executable
      },
      files: [
        '**/*', // Include all files in the build
        '!node_modules/**/*' // Exclude unnecessary files
      ]
    }
  }
}
