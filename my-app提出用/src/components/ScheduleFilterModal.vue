<template>
  <!-- モーダル背景 -->
  <div class="modal-overlay" @click="$emit('close')">
    <!-- モーダル本体 -->
    <div class="modal" @click.stop>
      <h3 class="modal-title">フィルター</h3>

<div class="modal-content">
  <!-- 種類フィルター -->
  <div class="filter-item">
    <label>種類：</label>
    <select :value="filterType" @change="$emit('update:filterType', $event.target.value)">
      <option value="all">全て</option>
      <option value="スケジュール">スケジュール</option>
      <option value="習慣">習慣</option>
    </select>
  </div>

  <!-- 時間帯フィルター（範囲指定） -->
  <div class="filter-item">
    <label>開始時刻：</label>
    <input type="time" :value="filterStartTime" @input="$emit('update:filterStartTime', $event.target.value)" />
    〜
    <input type="time" :value="filterEndTime" @input="$emit('update:filterEndTime', $event.target.value)" />
  </div>

  <!-- 完了状況フィルター -->
  <div class="filter-item">
    <label>完了：</label>
    <select :value="filterDone" @change="$emit('update:filterDone', $event.target.value)">
      <option value="all">全て</option>
      <option value="done">完了</option>
      <option value="undone">未完了</option>
    </select>
  </div>

  <!-- 重要度フィルター -->
  <div class="filter-item">
    <label>重要度：</label>
    <select :value="filterImportance" @change="$emit('update:filterImportance', $event.target.value)">
      <option value="all">全て</option>
      <option value="1">★1</option>
      <option value="2">★2</option>
      <option value="3">★3</option>
    </select>
  </div>

  <!-- キーワード検索 -->
  <div class="filter-item">
    <label>検索：</label>
    <input type="text" :value="filterKeyword" @input="$emit('update:filterKeyword', $event.target.value)" />
  </div>
</div>


      <!-- フッターボタン -->
      <div class="modal-footer">
        <button class="reset-btn" @click="resetFilters">リセット</button>
        <button class="close-btn" @click="$emit('close')">閉じる</button>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "ScheduleFilterModal",

  /**
   * props
   * -----------------
   * filterTimeZone: String
   *   - 現在選択されている時間帯フィルター値
   *   - 値例: "all", "morning", "noon", "evening", "night"
   * filterDone: String
   *   - 完了状況フィルター値
   *   - 値例: "all", "done", "undone"
   * filterImportance: String
   *   - 重要度フィルター値
   *   - 値例: "all", "1", "2", "3"
   * filterKeyword: String
   *   - 検索キーワード
   */
  props: {
    filterTimeZone: String,
    filterDone: String,
    filterImportance: String,
    filterKeyword: String,
    filterType: String,         // ← 追加
    filterStartTime: String,    // ← 追加
    filterEndTime: String       // ← 追加
  },
  emits: [
    "update:filterTimeZone",
    "update:filterDone",
    "update:filterImportance",
    "update:filterKeyword",
    "update:filterType",       // ← 追加
    "update:filterStartTime",  // ← 追加
    "update:filterEndTime",    // ← 追加
    "close"
  ],
  methods: {
    resetFilters() {
      // 全て初期値に戻す
      this.$emit("update:filterType", "all");
      this.$emit("update:filterStartTime", "");
      this.$emit("update:filterEndTime", "");
      this.$emit("update:filterDone", "all");
      this.$emit("update:filterImportance", "all");
      this.$emit("update:filterKeyword", "");
    }
  }
  /**
   * コンポーネントの役割・概要
   * -----------------
   * - タスクや習慣の一覧を絞り込み・検索するためのUI部品
   * - 親コンポーネントに対して v-model の双方向バインディングのように
   *   'update:〜' イベントを発火してフィルター状態を通知する
   * - 親側で受け取った値をもとにリスト表示を絞り込む
   *
   * 処理フロー:
   * 1. ユーザーが select または input を操作
   * 2. @change / @input イベントが発火
   * 3. $emit('update:フィルター名', 選択値) で親に通知
   * 4. 親コンポーネントで受け取り、表示リストを更新
   *
   * 返り値: なし（イベントで親に通知する方式）
   */
};
</script>


<style scoped>
/* モーダル背景 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

/* モーダル本体 */
.modal {
  background-color: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  width: 80vw;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  font-size: 1rem;
}

/* タイトル */
.modal-title {
  text-align: center;
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

/* 内容エリア */
.modal-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* フィルター1行ごとのスタイル */
.filter-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-item label {
  font-weight: 600;
  margin-right: 0.5rem;
}

.filter-item select,
.filter-item input {
  flex: 1;
  padding: 0.3rem 0.5rem;
}

/* フッター */
.modal-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.reset-btn {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 6px;
  border: none;
  background-color: #1976d2;
  color: #fff;
  cursor: pointer;
}

.close-btn {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 6px;
  border: none;
  background-color: #1976d2;
  color: #fff;
  cursor: pointer;
}
</style>