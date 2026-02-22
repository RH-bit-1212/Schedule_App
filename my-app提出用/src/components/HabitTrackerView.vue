<!--
==================================================
【概要】
習慣管理画面（今日の習慣一覧）を表示するコンポーネント。
・習慣データの取得（API）
・完了状態の更新
・新規作成／編集／削除
・詳細モーダル／編集モーダル制御
・URL（/habits/:id）とモーダル状態の同期
を担当する。

【親子コンポーネント構成】
[Parent]
- HabitPage（このコンポーネント）

[Children]
- HabitTable
  └ 習慣一覧表示、検索・並び替え・完了トグル
- HabitFormModal
  └ 新規登録・編集フォーム
- HabitDetailModal
  └ 習慣詳細表示・完了状態更新
==================================================
-->

<template>
  <section>
    <h2>🗓️ 今日の習慣（{{ todayStr }}）</h2>

    <!-- 検索・フィルター・並べ替えを HabitTable に渡す -->
    <HabitTable
      :habits="habits"
      :keyword="keyword"
      :sort-order="sortOrder"
      :importance-filter="importanceFilter"
      :done-filter="doneFilter"
      @row-click="openDetail"
      @update-done="saveHabits"
      @edit-habit="editHabit"
      @delete-habit="deleteHabit"
    />

    <!-- 新規登録/編集フォームモーダル -->
    <HabitFormModal
      v-if="showModalForm"
      :form-data="form"
      @save="saveForm"
      @close="closeFormModal"
    />

    <!-- 詳細表示モーダル -->
    <HabitDetailModal
      v-if="showModalDetail"
      :habit="selectedHabit"
      @close="closeDetail"
      @update-done="updateHabitDone"
    />

    <!-- 新規追加ボタン -->
    <button class="add-btn" @click="openFormModal">＋ 習慣を追加</button>

    <!-- 完了率表示 -->
    <div class="summary">
      完了済: {{ doneCount }} / 全{{ habits.length }}__
      達成率: {{ doneRate }}%
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchTasks, addTask, updateTask, deleteTask } from "@/api/api.js";

import HabitTable from "@/components/HabitTable.vue";
import HabitFormModal from "@/components/HabitFormModal.vue";
import HabitDetailModal from "@/components/HabitDetailModal.vue";

const route = useRoute();
const router = useRouter();

// ---------------------------
// データ（状態管理）
// ---------------------------
const habits = ref([]);
const todayStr = ref("");
const keyword = ref("");
const sortOrder = ref("asc");
const importanceFilter = ref("");
const doneFilter = ref("");

const showModalForm = ref(false);
const showModalDetail = ref(false);
const form = ref({ id: null, title: "", start: "00:00", end: "00:00", importance: 1, done: false });
const selectedHabit = ref(null);

/**
 * 【役割】：完了済み習慣の件数を算出する
 *
 * 【引数】：なし（habits を参照）
 *
 * 【処理フロー】
 * 1. habits 配列を走査
 * 2. done === true の要素数をカウント
 *
 * 【返り値】：number : 完了件数
 */
const doneCount = computed(() => habits.value.filter(h => h.done).length);

/**
 * 【役割】：習慣の達成率（％）を算出する
 *
 * 【引数】：なし
 *
 * 【処理フロー】
 * 1. 習慣が 0 件なら 0 を返す
 * 2. 完了数 / 全体数 * 100
 * 3. 四捨五入
 *
 * 【返り値】：number : 達成率（0〜100）
 */
const doneRate = computed(() =>
  habits.value.length === 0 ? 0 : Math.round((doneCount.value / habits.value.length) * 100)
);

// ========================
// CRUD メソッド
// ========================

/**
 * 【役割】
 * 習慣データを API から取得し画面に反映する
 * URL に id が含まれる場合は詳細モーダルを開く
 *
 * 【引数】：なし
 *
 * 【処理フロー】
 * 1. fetchTasks() で全タスク取得
 * 2. type === "習慣" のみ抽出
 * 3. URL パラメータに id があれば openDetail 実行
 *
 * 【返り値】：Promise<void>
 */
async function loadHabits() {
  const allTasks = await fetchTasks();
  habits.value = allTasks.filter(t => t.type === "習慣");

  const habitId = Number(route.params.id);
  if (habitId) openDetail(habitId, false);
}

/**
 * 【役割】：新規作成／編集フォームの内容を保存する
 *
 * 【引数】
 * habitFromModal : Object
 *  モーダルから渡された習慣データ
 *
 * 【処理フロー】
 * 1. 入力値を正規化（未入力補完）
 * 2. id があれば更新、なければ新規作成
 * 3. habits 配列を更新
 * 4. モーダルを閉じる
 *
 * 【返り値】：Promise<void>
 */
async function saveForm(habitFromModal) {
  const payload = {
    ...habitFromModal,
    title: habitFromModal.title || "未設定",
    start: habitFromModal.start || "00:00",
    end: habitFromModal.end || "00:00",
    importance: habitFromModal.importance || 1,
    type: "習慣",
  };

  if (payload.id) {
    await updateTask(payload.id, payload);
    const idx = habits.value.findIndex(h => h.id === payload.id);
    if (idx !== -1) habits.value[idx] = payload;
  } else {
    const newTask = await addTask(payload);
    habits.value.push(newTask);
  }
  closeFormModal();
}

/**
 * 【役割】：習慣の完了状態を更新する（詳細モーダルから）
 * 【引数】：updatedHabit : Object
 * 【処理フロー】
 * 1. API で更新
 * 2. habits 配列を同期
 * 3. 詳細表示用データを更新
 *
 * 【返り値】：Promise<void>
 */
async function updateHabitDone(updatedHabit) {
  await updateTask(updatedHabit.id, updatedHabit);
  const idx = habits.value.findIndex(h => h.id === updatedHabit.id);
  if (idx !== -1) habits.value[idx] = updatedHabit;
  selectedHabit.value = updatedHabit;
}

/**
 * 【役割】：習慣を削除する
 *
 * 【引数】：id : number
 *
 * 【処理フロー】
 * 1. 確認ダイアログ表示
 * 2. API で削除
 * 3. ローカル配列から除外
 * 4. 詳細モーダルを閉じる
 *
 * 【返り値】：Promise<void>
 */
async function deleteHabit(id) {
  if (!confirm("削除しますか？")) return;
  await deleteTask(id);
  habits.value = habits.value.filter(h => h.id !== id);
  closeDetail();
}

// ========================
// モーダル制御
// ========================

/**
 * 【役割】
 * 習慣詳細モーダルを開く
 *
 * 【引数】
 * idOrHabit : number | Object
 * pushUrl   : boolean（URL を更新するか）
 * 【処理フロー】
 * 1. id またはオブジェクトから習慣を特定
 * 2. selectedHabit にコピーを設定
 * 3. モーダル表示
 * 4. 必要に応じて URL 更新
 * 【返り値】：void
 */
const openDetail = (idOrHabit, pushUrl = true) => {
  let habit;
  if (typeof idOrHabit === "number") {
    habit = habits.value.find(h => h.id === idOrHabit);
  } else {
    habit = idOrHabit;
  }
  selectedHabit.value = habit ? { ...habit } : null;
  showModalDetail.value = !!habit;

  if (habit && pushUrl) router.push(`/habits/${habit.id}`);
};

/**
 * 【役割】：モーダルを閉じ、URL を一覧に戻す
 * 【引数】：なし
 * 【返り値】：void
 */
const closeDetail = () => {
  selectedHabit.value = null;
  showModalDetail.value = false;
  router.push("/habits");
};

/**
 * 【役割】：新規作成モーダルを開く
 * 【引数】：なし
 * 【返り値】：void
 */
const openFormModal = () => {
  form.value = { id: null, title: "", start: "00:00", end: "00:00", importance: 1, done: false };
  showModalForm.value = true;
};

/**
 * 【役割】：フォームモーダルを閉じる
 */
const closeFormModal = () => { showModalForm.value = false; };

/**
 * 【役割】：編集モードでフォームモーダルを開く
 * 【引数】：habit : Object
 */
const editHabit = (habit) => {
  form.value = { ...habit };
  showModalForm.value = true;
};

// ========================
// URL 直接アクセス対応
// ========================

/**
 * 【役割】：URL パラメータ変更に応じてモーダル状態を同期
 * 【引数】：newRoute : Route
 * 【返り値】：void
 */
watch(route, (newRoute) => {
  if (newRoute.params.id) {
    const habitId = Number(newRoute.params.id);
    openDetail(habitId, false);
  } else {
    selectedHabit.value = null;
    showModalDetail.value = false;
  }
});

// ========================
// ライフサイクル
// ========================

/**
 * 【役割】：初期表示処理
 *
 * 【処理フロー】
 * 1. 今日の日付文字列生成
 * 2. 習慣データ読み込み
 */
onMounted(() => {
  const today = new Date();
  const weekday = ["日","月","火","水","木","金","土"][today.getDay()];
  todayStr.value = `${today.getFullYear()}/${today.getMonth()+1}/${today.getDate()}（${weekday}）`;
  loadHabits();
});
</script>

<style scoped>
/* =========================
   習慣追加ボタン
========================= */
.add-btn {
  display: block;
  margin: 1.5rem auto 1rem; /* ← 中央配置 */
  padding: 0.9rem 7.0rem;
  border-radius: 10px;
  border: none;
  background-color: #4caf50;
  color: #fff;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
}

/* タップしやすく */
.add-btn:active {
  opacity: 0.85;
}

/* =========================
   達成率表示
========================= */
.summary {
  margin-top: 1rem;
  text-align: center;
  font-size: 1.6rem;
  font-weight: 600;
}

/* 達成率の数値を強調 */
.summary span {
  font-size: 2.3rem;
  font-weight: 800;
  color: #1976d2;
}

/* =========================
   スマホ微調整
========================= */
@media (max-width: 767px) {
  .add-btn {
    width: 90%;
    font-size: 1.3rem;
  }

  .summary {
    font-size: 1.6rem;
  }

  .summary span {
    font-size: 2.3rem;
  }
}

</style>
