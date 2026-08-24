# IELTS Mobile WebView Test

This Expo app loads the Flask project inside a WebView so it can be tested on a real phone using Expo Go.

## 1) Start the Flask backend

From the main project root:

```bash
cd "D:/New folder/IELTS_MASTER_HUB"
python app.py
```

The web app should be reachable from the network at something like:

```text
http://192.168.1.25:5000
```

Replace the IP with your computer's LAN IP.

## 2) Run the Expo app

```bash
cd "D:/New folder/IELTS_MASTER_HUB/expo-mobile"
npm install
npx expo start --lan
```

Scan the QR code in Expo Go on your phone.

## 3) Update the target URL

Edit [App.js](App.js) and replace the URL in:

```js
const WEBAPP_URL = 'http://192.168.1.25:5000';
```

or copy `.env.example` to `.env` and use it in the app if adapted.
