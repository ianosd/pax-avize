'use strict'

import { app, protocol, BrowserWindow, ipcMain, Menu } from 'electron'

import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
const isDevelopment = process.env.NODE_ENV !== 'production'

const path = require('path');
const fs = require('fs');
const https = require('https');

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

let win;

async function createWindow() {
  // Create the browser window.
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
      preload: path.join(__dirname, 'preload.js')
    }
  })

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }

  const menu = Menu.buildFromTemplate(createMenuTemplate());
  Menu.setApplicationMenu(menu);
}

function createMenuTemplate() {
  return [
    {
      label: "Setări",
      submenu: [
        {
          label: "Setează URL Server",
          click: () => {
            openUrlInputWindow();
          }
        },
        { type: "separator" },
        { role: "quit" }
      ]
    }
  ];
}

// Function to create a modal input window
function openUrlInputWindow() {
  const inputWindow = new BrowserWindow({
    width: 400,
    height: 200,
    modal: true,
    parent: win,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  inputWindow.loadURL(`data:text/html,
    <html>
      <body style="text-align: center; font-family: Arial;">
        <h3>Enter Base URL</h3>
        <input id="urlInput" type="text" style="width: 90%;" value="${getBaseURL()}"/>
        <br><br>
        <button onclick="saveUrl()">Save</button>
        <script>
          const { ipcRenderer } = require('electron');
          function saveUrl() {
            const url = document.getElementById("urlInput").value;
            ipcRenderer.send("set-base-url", url);
          }
        </script>
      </body>
    </html>
  `);

  // Handle URL update from renderer
  const { ipcMain } = require("electron");
  ipcMain.once("set-base-url", (_, url) => {
    if (url) {
      setBaseURL(url);
    }
    inputWindow.close();
  });
}

const iconName = path.join(__dirname, 'iconForDragAndDrop.png')
const icon = fs.createWriteStream(iconName)

// Create a new file to copy - you can also copy existing files.
fs.writeFileSync(path.join(__dirname, 'drag-and-drop-1.md'), '# First file to test drag and drop')
fs.writeFileSync(path.join(__dirname, 'drag-and-drop-2.md'), '# Second file to test drag and drop')

function getBaseURL(){
  try {
    const content =  fs.readFileSync(path.join(__dirname,'url.txt'), 'utf8');
    return content;
  } catch (e){
    console.log(e);
  }
  return "http://192.168.1.104:8082";
}

function setBaseURL(url) {
  fs.writeFileSync(path.join(__dirname, 'url.txt'), url);
}

https.get('https://img.icons8.com/ios/452/drag-and-drop.png', (response) => {
  response.pipe(icon)
})

ipcMain.on('ondragstart', (event, filePath) => {
  console.log(`filePath=${filePath}`);
  event.sender.startDrag({
    file: filePath,
    icon: iconName
  })
})

ipcMain.handle("get-base-url", getBaseURL);

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS3_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
