<!--
==================================================
【概要】
今日のスケジュール一覧を管理・表示する画面コンポーネント。
・スケジュール／習慣の統合表示
・複数条件によるフィルタリング
・新規作成／編集／削除
・詳細モーダル制御
・URL（/schedules/:id）とモーダル状態の同期
を担当する。

【親子コンポーネント構成】
[Parent]
- ScheduleView（このコンポーネント）

[Children]
- ScheduleFilter
  └ 時間帯・完了・重要度・キーワードのフィルター UI
- ScheduleForm
  └ スケジュール／習慣の登録・編集フォーム
- ScheduleTable
  └ フィルター後タスク一覧表示
- ScheduleDetailModal
  └ タスク詳細表示・編集・削除
==================================================
-->

<template>
  <section class="schedule-view">
    <!-- 今日の日付表示 -->
    <h2>🗓️ 今日のスケジュール（{{ todayStr }}）</h2>

    <!-- フィルターボタン + 作成ボタン -->
    <div class="action-btns-wrapper">
      <button class="filter-btn" @click="showFilterModal = true">🔍 フィルター</button>
      <button class="create-btn" @click="openCreateModal">＋ スケジュールを追加</button>
    </div>

    <!-- 一括操作バー -->
    <div class="bulk-action-bar">
      <!-- 選択削除 -->
      <button
        class="bulk-delete-btn"
        :disabled="selectedScheduleIds.length === 0"
        @click="bulkDeleteSchedules"
      >
        選択した {{ selectedScheduleIds.length }} 件を削除
      </button>

      <!-- 種類別 全削除 -->
      <button class="bulk-delete-btn danger" @click="deleteAllByType('スケジュール')">
        スケジュールを全削除
      </button>

      <button class="bulk-delete-btn danger" @click="deleteAllByType('習慣')">
        習慣を全削除
      </button>
    </div>



    <!-- 表示切替ボタン -->
    <div class="view-mode-buttons">
      <button @click="viewMode = 'table'">テーブル表示</button>
      <button @click="viewMode = 'list'">リスト表示</button>
      <button @click="viewMode = 'card'">カード表示</button>
      <button @click="viewMode = 'gantt'">ガントチャート</button>
    </div>

    <!-- 表示切替 -->
    <ScheduleTable
      v-if="viewMode === 'table'"
      :tasks="filteredTasks"
      :selected-ids="selectedScheduleIds"
      @update:selected-ids="selectedScheduleIds = $event"
      @row-click="openModal"
      @update-done="updateDone"
      @edit-task="editFromTable"
      @delete-task="deleteFromTable"
    />



    <ScheduleList
      v-if="viewMode === 'list'"
      :tasks="filteredTasks"
      @row-click="openModal"
      @update-done="updateDone"
    />


    <ScheduleCard
      v-if="viewMode === 'card'"
      :tasks="filteredTasks"
      @row-click="openModal"
      @update-done="updateDone"      
    />

    <ScheduleGantt
      v-if="viewMode === 'gantt'"
      :tasks="filteredTasks"
      @row-click="openModal"
      @update-done="updateDone"
    />

    <!-- フィルターモーダル -->
    <ScheduleFilterModal
      v-if="showFilterModal"
      :filter-time-zone="filterTimeZone"
      :filter-done="filterDone"
      :filter-importance="filterImportance"
      :filter-keyword="filterKeyword"
      :filter-type="filterType"
      :filter-start-time="filterStartTime"
      :filter-end-time="filterEndTime"
      @update:filterTimeZone="filterTimeZone = $event"
      @update:filterDone="filterDone = $event"
      @update:filterImportance="filterImportance = $event"
      @update:filterKeyword="filterKeyword = $event"
      @update:filterType="filterType = $event"
      @update:filterStartTime="filterStartTime = $event"
      @update:filterEndTime="filterEndTime = $event"
      @close="showFilterModal = false"
    />

    <!-- 詳細モーダル -->
    <ScheduleDetailModal
      v-if="modalTask"
      :task="modalTask"
      @close="closeModal"
      @edit="editFromModal"
      @delete="deleteFromModal"
      @update-done="updateDone"
    />

    <!-- 作成／編集フォームモーダル -->
    <ScheduleForm
      v-if="showFormModal"
      :form-data="form"
      @save="saveForm"
      @cancel="closeFormModal"
    />
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import ScheduleFilterModal from "./ScheduleFilterModal.vue";
import ScheduleForm from "./ScheduleForm.vue";
import ScheduleTable from "./ScheduleTable.vue";
import ScheduleList from "./ScheduleList.vue";
import ScheduleCard from "./ScheduleCard.vue";
import ScheduleGantt from "./ScheduleGantt.vue";
import ScheduleDetailModal from "./ScheduleDetailModal.vue";
import { fetchTasks, addTask, updateTask, deleteTask } from "../api/api.js";

// 複数選択（スケジュール・習慣 共通）
const selectedScheduleIds = ref([]);

// ---------------------------
// Vue Router
// ---------------------------
const route = useRoute();
const router = useRouter();

// ---------------------------
// データ（状態管理）
// ---------------------------
const schedules = ref([]);
const habits = ref([]);
const form = ref({
  id: null, title: "", start: "", end: "", memo: "",
  importance: 1, type: "スケジュール", done: false
});
const modalTask = ref(null);

const todayStr = ref("");
const filterTimeZone = ref("all");
const filterDone = ref("all");
const filterImportance = ref("all");
const filterKeyword = ref("");
const filterType = ref("all");        // 種類フィルター
const filterStartTime = ref("");      // 開始時刻
const filterEndTime = ref("");        // 終了時刻


// フォームモーダル表示制御
const showFormModal = ref(false);

// フィルターモーダル表示制御
const showFilterModal = ref(false);

const viewMode = ref("table");

// ============================
// フィルタリング
// ============================

/**
 * 【役割】
 * スケジュールと習慣を結合した全タスク一覧を生成する
 *
 * 【引数】
 * なし
 *
 * 【返り値】
 * Array : 全タスク配列
 */
const allTasks = computed(() => [...schedules.value, ...habits.value]);

/**
 * 【役割】
 * フィルター条件を適用したタスク一覧を生成する
 *
 * 【引数】
 * なし
 *
 * 【処理フロー】
 * 1. 完了状態フィルター
 * 2. 重要度フィルター
 * 3. キーワード検索
 * 4. 時間帯フィルター
 * 5. 開始時刻順にソート
 *
 * 【返り値】
 * Array : フィルター済みタスク
 */
const filteredTasks = computed(() => applyFilters(allTasks.value));

/**
 * 【役割】
 * 指定されたタスクリストにフィルター条件を適用する
 *
 * 【引数】
 * list : Array
 *
 * 【返り値】
 * Array : フィルター済みリスト
 */
function applyFilters(list) {
  let result = [...list];

  // 種類フィルター
  if (filterType.value !== "all") {
    result = result.filter(t => t.type === filterType.value);
  }

  // 完了フィルター
  if (filterDone.value === "done") result = result.filter(t => t.done);
  if (filterDone.value === "undone") result = result.filter(t => !t.done);

  if (filterImportance.value !== "all") {
    result = result.filter(t => Number(t.importance) === Number(filterImportance.value));
  }

  // 重要度
  if (filterKeyword.value.trim() !== "") {
    const kw = filterKeyword.value.toLowerCase();
    result = result.filter(
      t =>
        t.title.toLowerCase().includes(kw) ||
        (t.memo && t.memo.toLowerCase().includes(kw))
    );
  }

  // 時間帯（範囲）
  if (filterStartTime.value) {
    result = result.filter(t => t.start >= filterStartTime.value);
  }
  if (filterEndTime.value) {
    result = result.filter(t => t.end <= filterEndTime.value);
  }

  return result.sort((a, b) => a.start.localeCompare(b.start));
}


// ============================
// CRUD
// ============================

/**
 * 【役割】
 * API からタスク一覧を取得し初期状態を構築する
 *
 * 【処理フロー】
 * 1. fetchTasks() 実行
 * 2. スケジュール／習慣を分類
 * 3. URL に id があれば詳細モーダル表示
 *
 * 【返り値】
 * Promise<void>
 */
async function loadData() {
  const tasks = await fetchTasks();
  schedules.value = tasks.filter(t => t.type === "スケジュール");
  habits.value = tasks.filter(t => t.type === "習慣");

  const taskId = Number(route.params.id);
  if (taskId) openModal(taskId, false);
}


function openCreateModal() {
  cancelEdit();          // フォーム初期化
  showFormModal.value = true;
}

function closeFormModal() {
  showFormModal.value = false;
}

/**
 * 【役割】
 * フォーム入力内容を保存（新規作成／更新）
 *
 * 【引数】
 * task : Object
 *
 * 【返り値】
 * Promise<void>
 */
async function saveForm(task) {
  try {
    if (task.id) {
      const updated = await updateTask(task.id, task);
      const target = task.type === "スケジュール" ? schedules.value : habits.value;
      const idx = target.findIndex(t => t.id === task.id);
      if (idx !== -1) target[idx] = updated;
    } else {
      const created = await addTask(task);
      if (task.type === "スケジュール") schedules.value.push(created);
      else habits.value.push(created);
    }
    closeFormModal();
  } catch (e) {
    console.error("保存エラー:", e);
  }
}


/**
 * 【役割】
 * タスクの完了状態を更新する
 *
 * 【引数】
 * task : Object
 *
 * 【返り値】
 * Promise<void>
 */
async function updateDone(task) {
  try {
    const updated = await updateTask(task.id, task);
    const target = task.type === "スケジュール" ? schedules.value : habits.value;
    const idx = target.findIndex(t => t.id === task.id);
    if (idx !== -1) target[idx] = updated;

    if (modalTask.value?.id === updated.id) {
      modalTask.value = updated;
    }
  } catch (e) {
    console.error("更新エラー:", e);
  }
}

/**
 * 【役割】
 * 指定 ID のタスクを削除する
 *
 * 【引数】
 * id   : number
 * type : string
 *
 * 【返り値】
 * Promise<void>
 */
async function deleteTaskById(id, type) {
  if (!confirm("削除しますか？")) return;

  try {
    await deleteTask(id);

    if (type === "スケジュール") {
      schedules.value = schedules.value.filter(t => t.id !== id);
      selectedScheduleIds.value =
        selectedScheduleIds.value.filter(v => v !== id);
    } else {
      habits.value = habits.value.filter(t => t.id !== id);
    }

    closeModal();
  } catch (e) {
    console.error("削除エラー:", e);
  }
}


// ============================
// モーダル操作
// ============================

/**
 * 【役割】
 * 詳細モーダルを開く
 *
 * 【引数】
 * taskOrId : Object | number
 * pushUrl  : boolean
 *
 * 【返り値】
 * void
 */
function openModal(taskOrId, pushUrl = true) {
  let task;
  if (typeof taskOrId === "number") {
    task = schedules.value.find(t => t.id === taskOrId)
        || habits.value.find(t => t.id === taskOrId);
  } else {
    task = taskOrId;
  }
  modalTask.value = task ? { ...task } : null;

  if (task && pushUrl) router.push(`/schedules/${task.id}`);
}

/**
 * 【役割】
 * 詳細モーダルを閉じ、URL を一覧に戻す
 */
function closeModal() {
  modalTask.value = null;
  router.push("/schedules");
}

function editFromModal(task) { form.value = { ...task }; showFormModal.value = true; closeModal(); }
function deleteFromModal(id, type) { deleteTaskById(id, type); }
function editFromTable(task) { form.value = { ...task }; showFormModal.value = true; }
function deleteFromTable(id, type) { deleteTaskById(id, type); }

/**
 * 【役割】
 * フォームを初期状態に戻す
 */
function cancelEdit() {
  closeFormModal();
  form.value = {
    id: null, title: "", start: "", end: "",
    memo: "", importance: 1, type: "スケジュール", done: false
  };
}


// ============================
// ライフサイクル
// ============================

/**
 * 【役割】
 * 初期表示処理
 */
onMounted(() => {
  const today = new Date();
  const weekday = ["日","月","火","水","木","金","土"][today.getDay()];
  todayStr.value = `${today.getFullYear()}/${today.getMonth()+1}/${today.getDate()}（${weekday}）`;
  loadData();
});

/**
 * 【役割】
 * URL 直接アクセス時に詳細モーダルを同期する
 */
watch(route, (newRoute) => {
  if (newRoute.params.id) {
    const taskId = Number(newRoute.params.id);
    openModal(taskId, false);
  } else {
    modalTask.value = null;
  }
});

watch(filteredTasks, () => {
  selectedScheduleIds.value = [];
});

watch(viewMode, () => {
  selectedScheduleIds.value = [];
});


/**
 * 【役割】
 * 選択されたタスク（スケジュール・習慣）を一括削除する
 */
async function bulkDeleteSchedules() {
  const count = selectedScheduleIds.value.length;
  if (count === 0) return;

  if (!confirm(`${count}件のタスクを削除しますか？`)) return;

  try {
    // API削除
    for (const id of selectedScheduleIds.value) {
      await deleteTask(id);
    }

    // ★ ここが重要：両方から削除する
    schedules.value = schedules.value.filter(
      t => !selectedScheduleIds.value.includes(t.id)
    );

    habits.value = habits.value.filter(
      t => !selectedScheduleIds.value.includes(t.id)
    );

    selectedScheduleIds.value = [];

    // 詳細モーダルが削除対象なら閉じる
    if (
      modalTask.value &&
      ![...schedules.value, ...habits.value].some(t => t.id === modalTask.value.id)
    ) {
      closeModal();
    }

  } catch (e) {
    console.error("一括削除エラー:", e);
  }
}



/**
 * 【役割】
 * 指定タイプのタスクを全削除する
 *
 * @param {string} type "スケジュール" | "習慣"
 */
async function deleteAllByType(type) {
  const targets = type === "スケジュール"
    ? schedules.value
    : habits.value;

  if (targets.length === 0) {
    alert(`${type}は存在しません`);
    return;
  }

  if (!confirm(`${type}を ${targets.length} 件すべて削除しますか？`)) return;

  try {
    for (const task of targets) {
      await deleteTask(task.id);
    }

    if (type === "スケジュール") {
      schedules.value = [];
    } else {
      habits.value = [];
    }

    // 詳細モーダルが該当タイプなら閉じる
    if (modalTask.value?.type === type) {
      closeModal();
    }
  } catch (e) {
    console.error("一括削除エラー:", e);
  }
}


</script>

<style scoped>
.schedule-view h2 {
  font-size: 1.3rem; /* お好みのサイズに変更 */
  font-weight: 600;  /* 太さも調整可能 */
  margin-bottom: 1rem;
}

.schedule-view { padding: 1rem; }
.schedule-wrapper { display: flex; gap: 1rem; }

.action-btns-wrapper {
  display: flex;
  gap: 1rem;       /* ボタン間の間隔 */
  margin: 1rem 0;
}

.filter-btn,
.create-btn {
  padding: 0.8rem 1.6rem;
  font-size: 1.1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.filter-btn {
  background-color: #ff5555ff;
  color: #ffffffff;
}

.create-btn {
  background-color: #1976d2;
  color: #fff;
}


.bulk-delete-btn.danger {
  background-color: #d9534f;
  color: white;
}
</style>
