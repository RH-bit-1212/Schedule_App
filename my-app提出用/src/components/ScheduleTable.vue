<template>
  <div class="table-wrapper">
    <table class="habit-table">
      <thead>
        <tr>
          <!-- 複数選択用チェック -->
          <th class="select-col">選択</th>

          <!-- 完了 -->
          <th class="check-col">✔</th>

          <th>タスク</th>
          <th>時間帯</th>
          <th>重要度</th>
          <th class="action-col">操作</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="task in tasks"
          :key="task.id"
          class="click-row"
          :class="[
            task.type === 'スケジュール' ? 'schedule-row' : 'habit-row',
            selectedIds.includes(task.id) ? 'selected-row' : ''
          ]"
          @click="$emit('row-click', task)"
        >
          <!-- 複数選択チェックボックス -->
          <td class="select-col" @click.stop>
            <input
              type="checkbox"
              :checked="selectedIds.includes(task.id)"
              @change="toggleSelect(task.id)"
            />
          </td>

          <!-- 完了チェック -->
          <td class="check-col" @click.stop>
            <input
              type="checkbox"
              :checked="task.done"
              @change="$emit('update-done', { ...task, done: !task.done })"
            />
          </td>

          <!-- タスク名 -->
          <td :class="{ done: task.done }">
            {{ task.title || '未設定' }}
          </td>

          <!-- 時間 -->
          <td>
            {{ task.start || '00:00' }} ~ {{ task.end || '00:00' }}
          </td>

          <!-- 重要度 -->
          <td class="stars">
            {{ '★'.repeat(task.importance || 1) }}
          </td>

          <!-- 操作 -->
          <td class="action-col">
            <button
              class="edit-btn"
              @click.stop="$emit('edit-task', task)"
            >
              ✏️
            </button>
            <button
              class="delete-btn"
              @click.stop="$emit('delete-task', task.id, task.type)"
            >
              🗑️
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "ScheduleTable",

  /**
   * props
   * -----------------
   * tasks        : 表示するタスク一覧
   * selectedIds  : 親で管理している選択中スケジュールID配列
   */
  props: {
    tasks: {
      type: Array,
      required: true
    },
    selectedIds: {
      type: Array,
      required: true
    }
  },

  /**
   * emits
   * -----------------
   * update:selected-ids : 複数選択変更通知
   * row-click           : 行クリック（詳細表示）
   * update-done         : 完了状態更新
   * edit-task           : 編集
   * delete-task         : 削除
   */
  emits: [
    "update:selected-ids",
    "row-click",
    "update-done",
    "edit-task",
    "delete-task"
  ],

  methods: {
    /**
     * 複数選択トグル
     */
    toggleSelect(id) {
      const next = this.selectedIds.includes(id)
        ? this.selectedIds.filter(v => v !== id)
        : [...this.selectedIds, id];

      this.$emit("update:selected-ids", next);
    }
  }
};
</script>

<style scoped>
/* =========================
   テーブルスクロール領域
========================= */
.table-wrapper {
  height: 100%;
  max-height: calc(100vh - 300px);
  overflow-y: auto;
  overflow-x: auto;
}

/* =========================
   テーブル
========================= */
.habit-table {
  width: 70%;
  min-width: 600px;
  border-collapse: collapse;
  margin: 0 auto;
}

th,
td {
  border: 1px solid #ccc;
  padding: 0.6rem;
  font-size: 1rem;
  text-align: left;
  vertical-align: middle;
}

/* =========================
   行クリック
========================= */
.click-row {
  cursor: pointer;
}

.click-row:hover {
  background-color: #f5f5f5;
}

/* =========================
   完了状態
========================= */
.done {
  text-decoration: line-through;
  color: #888;
}

/* =========================
   チェック列
========================= */
.check-col {
  width: 60px;
  text-align: center;
}

.check-col input[type="checkbox"] {
  transform: scale(1.6);
  cursor: pointer;
}

/* =========================
   操作列
========================= */
.action-col {
  width: 120px;
  text-align: center;
}

.action-col button {
  padding: 0.5rem 0.7rem;
  font-size: 1.1rem;
  margin: 0 0.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

/* 編集 */
.edit-btn {
  background-color: #71b1dfff;
}

/* 削除 */
.delete-btn {
  background-color: #ce6676ff;
}

/* =========================
   重要度
========================= */
.stars {
  color: #f57c00;
  letter-spacing: 2px;
}

/* スケジュール（水色） */
.schedule-row {
  background-color: #e3f2fd; /* 水色 */
}

/* 習慣（ピンク） */
.habit-row {
  background-color: #ffe3e3; /* ピンク */
}


/* =========================
   スマホ補正
========================= */
@media (max-width: 767px) {
  th,
  td {
    padding: 0.8rem;
    font-size: 1.05rem;
  }

  .action-col button {
    padding: 0.7rem;
    font-size: 1.2rem;
  }
}
</style>
