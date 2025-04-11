const { contextBridge, ipcRenderer } = require('electron');
http = require('http');
fs = require('fs');
path = require('path');

contextBridge.exposeInMainWorld('electron', {
      startDrag: (url) => {
            http.get(url, response => {
                  if (response.statusCode !== 200) {
                        console.error(`Failed to get data. Status code: ${response.statusCode}`);
                        return;
                  }

                  const filePath = "aviz.xml"
                  const file = fs.createWriteStream(filePath);
                  response.pipe(file);

                  file.on('finish', () => {
                        file.close();
                        ipcRenderer.send('ondragstart', filePath)
                        console.log(`Data saved to ${filePath}`);
                  });
            }).on('error', (err) => {
                  console.error(`Error: ${err.message}`);
            });
      },
      getBaseUrl: () => ipcRenderer.invoke("get-base-url")
})