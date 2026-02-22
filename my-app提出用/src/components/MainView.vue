<!--
==================================================
【概要】
今日のスケジュール画面を制御するコンポーネント。
・現在時刻の取得と監視
・進行中タスクの抽出
・全タスク一覧の取得と表示制御
・完了状態の更新
・DailySchedule の表示インデックス管理
を担当する。

【親子コンポーネント構成】
[Parent]
- DailyPage（このコンポーネント）

[Children]
- ClockComponent
  └ 現在時刻を定期的に通知
- CurrentTasks
  └ 現在進行中のタスク一覧表示
- DailySchedule
  └ 今日の全スケジュールを順送り表示
==================================================
-->

<template>
  <section class="dashboard">
    <!-- ヘッダー（時計） -->
    <header class="dashboard-header">
      <ClockComponent @time-changed="onTimeChanged" />
    </header>

    <!-- スクロール可能：現在の予定 -->
    <main class="dashboard-main">
      <CurrentTasks
        :tasks="currentTasks"
        @update-done="updateDone"
      />
    </main>

    <!-- フッター（今日のスケジュール） -->
    <footer class="dashboard-footer">
      <DailySchedule
        :tasks="allTasks"
        :view-index="viewIndex"
        @prev="prevTask"
        @next="nextTask"
      />
    </footer>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

import ClockComponent from "@/components/Clock.vue";
import CurrentTasks from "@/components/CurrentTasks.vue";
import DailySchedule from "@/components/DailySchedule.vue";

import { fetchTasks, updateTask } from "@/api/api.js";

// ================================
// state（状態管理）
// ================================
const tasks = ref([]);
const currentTasks = ref([]);
const allTasks = ref([]);
const viewIndex = ref(0);

const route = useRoute();

// ================================
// functions
// ================================

/**
 * 【役割】
 * 現在時刻を HH:mm 形式で取得する
 *
 * 【引数】
 * なし
 *
 * 【処理フロー】
 * 1. Date オブジェクト生成
 * 2. 時・分をゼロ埋め
 * 3. "HH:mm" 形式の文字列を生成
 *
 * 【返り値】
 * string : 現在時刻（例 "09:30"）
 */
function getCurrentTime() {
  const now = new Date();
  return `${String(now.getHours()).padStart(2,"0")}:${String(now.getMinutes()).padStart(2,"0")}`;
}

/**
 * 【役割】
 * API からタスク一覧を取得し初期表示状態を構築する
 *
 * 【引数】
 * なし
 *
 * 【処理フロー】
 * 1. fetchTasks() で全タスク取得
 * 2. 必要なプロパティを付与
 * 3. 開始時刻順にソート
 * 4. allTasks / viewIndex を初期化
 * 5. 現在進行中タスクを算出
 *
 * 【返り値】
 * Promise<void>
 */
async function loadData() {
  try {
    const data = await fetchTasks();
    tasks.value = data.map(t => ({
      ...t,
      type: t.type // API 側で "スケジュール" / "習慣" を想定
    }));

    // 時刻順にソート
    tasks.value.sort((a, b) => a.start.localeCompare(b.start));
    allTasks.value = [...tasks.value];

    if (viewIndex.value >= allTasks.value.length) {
      viewIndex.value = allTasks.value.length - 1;
    }

    // 現在進行中タスクを初期化
    onTimeChanged(getCurrentTime());

  } catch (err) {
    console.error("タスク取得エラー:", err);
  }
}

/**
 * 【役割】
 * 現在時刻に応じて進行中タスクを抽出する
 *
 * 【引数】
 * currentTime : string（HH:mm）
 *
 * 【処理フロー】
 * 1. tasks を走査
 * 2. start <= 現在時刻 <= end のタスクを抽出
 *
 * 【返り値】
 * void（currentTasks を更新）
 */
function onTimeChanged(currentTime) {
  currentTasks.value = tasks.value.filter(
    t => t.start <= currentTime && currentTime <= t.end
  );
}

/**
 * 【役割】
 * タスクの完了状態を更新する
 *
 * 【引数】
 * task : Object
 *
 * 【処理フロー】
 * 1. API に完了状態を送信
 * 2. ローカル tasks を更新
 * 3. 現在進行中タスクを再計算
 *
 * 【返り値】
 * Promise<void>
 */
async function updateDone(task) {
  try {
    await updateTask(task.id, { ...task, done: task.done });

    const idx = tasks.value.findIndex(t => t.id === task.id);
    if (idx !== -1) tasks.value[idx] = { ...task };

    onTimeChanged(getCurrentTime());
  } catch (err) {
    console.error("タスク更新エラー:", err);
  }
}

/**
 * 【役割】
 * DailySchedule の表示対象を前に移動する
 *
 * 【引数】
 * なし
 *
 * 【返り値】
 * void
 */
function prevTask() {
  if (viewIndex.value > 0) viewIndex.value--;
}

/**
 * 【役割】
 * DailySchedule の表示対象を次に移動する
 *
 * 【引数】
 * なし
 *
 * 【返り値】
 * void
 */
function nextTask() {
  if (viewIndex.value < allTasks.value.length - 1) viewIndex.value++;
}

// ================================
// URL 監視（拡張用）
// ================================

/**
 * 【役割】
 * URL クエリに応じて表示タスクを切り替える
 *
 * 【引数】
 * newRoute : Route
 *
 * 【処理フロー】
 * 1. highlightTask クエリを取得
 * 2. 該当タスクがあれば viewIndex を更新
 *
 * 【返り値】
 * void
 */
watch(route, (newRoute) => {
  const taskId = newRoute.query.highlightTask;
  if (taskId) {
    const idx = tasks.value.findIndex(t => t.id === Number(taskId));
    if (idx !== -1) viewIndex.value = idx;
  }
});

// ================================
// mounted
// ================================

/**
 * 【役割】
 * 初期表示時にタスクデータを取得する
 *
 * 【返り値】
 * void
 */
onMounted(() => {
  loadData();
});
</script>

<style scoped>
/* =========================
   全体レイアウト
========================= */
.dashboard {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px); /* ← 重要 */
  overflow: hidden;
}

/* =========================
   ヘッダー（時計）
========================= */
.dashboard-header {
  flex-shrink: 0;
  padding: 8px;
  border-bottom: 1px solid #ddd;
  background-color: #fff;
  z-index: 10;
}

/* =========================
   メイン（現在の予定）
========================= */
.dashboard-main {
  height: calc(100vh - 64px - 64px - 16px);
  overflow-y: auto;
}


/* =========================
   フッター（今日の予定）
========================= */
.dashboard-footer {
  flex-shrink: 0;
  padding: 8px;
  border-top: 1px solid #ddd;
  background-color: #fff;
}

/* =========================
   スマホ微調整
========================= */
@media (max-width: 767px) {
  .dashboard-header,
  .dashboard-footer {
    padding: 6px;
  }

  .dashboard-main {
    padding: 6px;
  }
}

</style>
