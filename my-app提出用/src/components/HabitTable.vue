<template>
  <div class="table-wrapper">
    <table class="habit-table">
      <thead>
        <tr>
          <th class="check-col">✔</th>
          <th>習慣</th>
          <th>時間帯</th>
          <th>重要度</th>
          <th class="action-col">操作</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="habit in filteredHabits"
          :key="habit.id"
          class="click-row"
          @click="$emit('row-click', habit)"
        >
          <!-- チェック（行クリック無効） -->
          <td class="check-col" @click.stop>
            <input
              type="checkbox"
              v-model="habit.done"
              @change.stop="$emit('update-done', habit)"
            />
          </td>

          <td :class="{ done: habit.done }">
            {{ habit.title || '未設定' }}
          </td>

          <td>
            {{ habit.start || '00:00' }} ~ {{ habit.end || '00:00' }}
          </td>

          <td class="stars">
            {{ '★'.repeat(habit.importance || 1) }}
          </td>

          <!-- 操作ボタン -->
          <td class="action-col" @click.stop>
            <button
              class="edit-btn"
              @click="$emit('edit-habit', habit)"
            >
              ✏️
            </button>
            <button
              class="delete-btn"
              @click="$emit('delete-habit', habit.id)"
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
  name: "HabitTable", // コンポーネント名

  // props: 親コンポーネントから渡される情報
  props: {
    habits: { type: Array, default: () => [] },  // 習慣の配列
    keyword: { type: String, default: "" },     // 検索キーワード
    sortOrder: { type: String, default: "asc" },// ソート順
    importanceFilter: { type: String, default: "" }, // 重要度フィルター
    doneFilter: { type: String, default: "" }   // 完了フィルター
  },

  // computed: 依存する値が変化したときに自動で計算されるプロパティ
  computed: {

    /**
     * filteredHabits
     * -----------------
     * フィルタリング・ソート済みの習慣リストを返す
     * 処理フロー:
     *   1. props.habits をコピーして list に代入
     *   2. keyword が指定されていればタイトルに含まれるものだけ抽出
     *   3. importanceFilter が指定されていれば該当重要度だけ抽出
     *   4. doneFilter が指定されていれば完了/未完了で抽出
     *   5. sortOrder に従って start 時間で昇順/降順ソート
     * 返り値:
     *   フィルタリング・ソート済みの配列
     */
    filteredHabits() {
      let list = [...this.habits];


      // キーワード検索
      if (this.keyword.trim() !== "") {
        const kw = this.keyword.toLowerCase();
        list = list.filter(h => h.title && h.title.toLowerCase().includes(kw));
      }

      // 重要度フィルター
      if (this.importanceFilter !== "") {
        list = list.filter(h => String(h.importance) === this.importanceFilter);
      }

      // 完了フィルター
      if (this.doneFilter !== "") {
        const doneVal = this.doneFilter === "true";
        list = list.filter(h => h.done === doneVal);
      }

      // 時間帯でソート
      list.sort((a, b) =>
        this.sortOrder === "asc" ? a.start.localeCompare(b.start) : b.start.localeCompare(a.start)
      );

      return list;
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
  /* ↑
     ヘッダー + フッター + 余白分を引く
     （環境により 200〜260px で微調整）
  */

  overflow-y: auto;   /* ← 縦スクロールはここだけ */
  overflow-x: auto;   /* 横は従来通り */
}


/* =========================
   テーブル
========================= */
.habit-table {
  width: 70%;
  border-collapse: collapse;
  min-width: 600px; /* スマホ横スクロール前提 */
  margin: 0 auto;            /* ← 左右中央配置 */
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

/* チェックボックス拡大 */
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

/* ボタン共通 */
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
