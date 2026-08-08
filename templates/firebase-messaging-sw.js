 
importScripts(
    "https://www.gstatic.com/firebasejs/12.1.0/firebase-app-compat.js"
);

importScripts(
    "https://www.gstatic.com/firebasejs/12.1.0/firebase-messaging-compat.js"
);

firebase.initializeApp({
    apiKey: "AIzaSyBYrN3awQ6KwAL4Ox6A0rc7O0AnGclMXHg",
    authDomain: "garda-a8eb9.firebaseapp.com",
    projectId: "garda-a8eb9",
    storageBucket: "garda-a8eb9.firebasestorage.app",
    messagingSenderId: "615899913660",
    appId: "1:615899913660:web:593bb216ae08d3503a5fb9"
});
console.log("🔥 FIREBASE SERVICE WORKER LOADED");

const messaging = firebase.messaging();

console.log("🔥 Firebase Messaging initialized");

messaging.onBackgroundMessage((payload) => {
    console.log(
        "🔥 FCM BACKGROUND MESSAGE:",
        payload
    );

    const title =
        payload.notification?.title || "GardaKSB";

    const options = {
        body: payload.notification?.body || "",
        data: payload.data || {}
    };

    self.registration.showNotification(
        title,
        options
    );
});