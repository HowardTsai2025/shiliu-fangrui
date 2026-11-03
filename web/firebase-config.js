// Firebase 設定（用來讓大家登入 Google 保存進度）
// 這段是公開資料（像網站的門牌地址），不是密碼；真正把關的是 firestore.rules。
// 改成 null 就會關掉 Google 登入，網站照常可以閱讀，大家用「進度碼」備份。
window.FIREBASE_CONFIG = {
  apiKey: "AIzaSyDi1VUUS-6uBzLunz4VBUqyePE3GA9-XT8",
  authDomain: "shi-liu-fang-rui.firebaseapp.com",
  projectId: "shi-liu-fang-rui",
  storageBucket: "shi-liu-fang-rui.firebasestorage.app",
  messagingSenderId: "594913543326",
  appId: "1:594913543326:web:6eca5415fd88789929a78f"
};
