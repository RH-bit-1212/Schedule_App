<template>
  <div class="app-container">
    <component :is="views[currentView]" />

    <footer class="footer-nav">
      <div class="footer-inner">
        <button @click="showView('MainView', '/')">メイン</button>
        <button @click="showView('HabitTrackerView', '/habits')">習慣</button>
        <button @click="showView('ScheduleView', '/schedules')">スケジュール</button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MainView from './components/MainView.vue'
import HabitTrackerView from './components/HabitTrackerView.vue'
import ScheduleView from './components/ScheduleView.vue'

// インポートしたコンポーネントをオブジェクトにまとめる
const views = { MainView, HabitTrackerView, ScheduleView }

const currentView = ref('MainView')
const router = useRouter()

const showView = (viewName, path) => {
  currentView.value = viewName
  // URL を遷移（実際にブラウザ履歴も残る）
  router.push(path)
}
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
  overflow: hidden;
}

/* ===== 全体 ===== */
.app-container {
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* ===== フッター外枠 ===== */
.footer-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 64px;
  background-color: #ffffff;
  border-top: 1px solid #ccc;
  display: flex;
  justify-content: center;
}

/* ===== フッター内側（PC大画面対応） ===== */
.footer-inner {
  width: 100%;
  max-width: 1400px; /* ← 大画面PC対応 */
  display: flex;
}

/* ===== ボタン ===== */
.footer-inner button {
  flex: 1;
  border: none;
  background-color: transparent;
  font-size: 15px;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s, color 0.2s;
}

/* 縦区切り線 */
.footer-inner button:not(:last-child)::after {
  content: "";
  position: absolute;
  top: 15%;
  right: 0;
  width: 1px;
  height: 70%;
  background-color: #ddd;
}

/* ホバー */
.footer-inner button:hover {
  background-color: #5c6f8bff;
  color: #ffffffff;
}

/* アクティブ（後で currentView と連動） */
.footer-inner button.active {
  background-color: #e3f2fd;
  color: #1976d2;
  font-weight: 600;
}

/* ===== PCレイアウト微調整 ===== */
@media (min-width: 1024px) {
  .footer-inner button {
    font-size: 16px;
  }
}
</style>