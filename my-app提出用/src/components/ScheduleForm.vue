<template>
  <!-- モーダル背景 -->
  <div class="modal-overlay" @click="$emit('cancel')">
    <!-- モーダル本体 -->
    <div class="modal" @click.stop>
      <!-- タイトル -->
      <h3 class="modal-title">
        {{ localForm.id ? 'スケジュールを編集' : 'スケジュールを追加' }}
      </h3>

      <!-- フォーム -->
      <form class="form-content" @submit.prevent="save">
        <!-- タイトル -->
        <div class="form-item">
          <label>タイトル</label>
          <input v-model="localForm.title" required />
        </div>

        <!-- 開始 -->
        <div class="form-item">
          <label>開始</label>
          <input type="time" v-model="localForm.start" required />
        </div>

        <!-- 終了 -->
        <div class="form-item">
          <label>終了</label>
          <input type="time" v-model="localForm.end" required />
        </div>

        <!-- 重要度 -->
        <div class="form-item">
          <label>重要度</label>
          <select v-model="localForm.importance">
            <option value="1">★</option>
            <option value="2">★★</option>
            <option value="3">★★★</option>
          </select>
        </div>

        <!-- メモ -->
        <div class="form-item">
          <label>メモ</label>
          <textarea v-model="localForm.memo" rows="4" />
        </div>

        <!-- 種類 -->
        <div class="form-item">
          <label>種類</label>
          <select v-model="localForm.type">
            <option value="スケジュール">スケジュール</option>
            <option value="習慣">習慣</option>
          </select>
        </div>

        <!-- ボタン -->
        <div class="form-buttons">
          <button type="submit" class="save-btn">保存</button>
          <button type="button" class="cancel-btn" @click="$emit('cancel')">
            キャンセル
          </button>
        </div>
      </form>
    </div>
  </div>
</template>


<script>
export default {
  name: "ScheduleForm",

  /**
   * props
   * -----------------
   * formData: Object
   *   - 編集または新規追加用のタスク/習慣データ
   *   - { id, title, start, end, importance, memo, type }
   */

  props: { formData: Object },

  /**
   * emits
   * -----------------
   * save  : 保存時に localForm の内容を親に送信
   * cancel: キャンセル時に親に通知
   */
  emits: ["save", "cancel"],

  /**
   * data
   * -----------------
   * localForm: Object
   *   - フォーム用ローカルコピー
   *   - props.formData をコピーして使用（親のデータを直接変更しないため）
   */
  data() {
    return { localForm: { ...this.formData } };
  },

  /**
   * watch
   * -----------------
   * props.formData を監視して、更新があれば localForm を再コピー
   * 引数:
   *   newVal: 更新された formData
   * 処理フロー:
   *   1. formData が変更される
   *   2. localForm を新しい値で上書き
   * 返り値: なし
   */
  watch: {
    formData: {
      handler(newVal) {
        this.localForm = { ...newVal };
      },
      deep: true,
    },
  },

  /**
   * methods
   * -----------------
   * save: 保存処理
   * 引数: なし（フォームデータは localForm に格納）
   * 処理フロー:
   *   1. localForm の内容をコピーして親に emit('save', data)
   *   2. 親コンポーネントで保存処理や localStorage 更新を行う
   * 返り値: なし
   */
  methods: {
    save() { 
      this.$emit("save", { ...this.localForm }); 
    }
  }
};
</script>

<style scoped>
/* =========================
   モーダル背景
========================= */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

/* =========================
   モーダル本体
========================= */
.modal {
  background: #fff;
  border-radius: 12px;
  padding: 1.6rem;
  width: 80%;
  max-width: 600px;
  font-size: 1.05rem;
}

/* =========================
   タイトル
========================= */
.modal-title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
}

/* =========================
   フォーム
========================= */
.form-content {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

label {
  font-weight: 700;
  font-size: 1.1rem;
  color: #555;
}

input,
select,
textarea {
  padding: 0.6rem;
  font-size: 1.05rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

/* =========================
   ボタン
========================= */
.form-buttons {
  display: flex;
  justify-content: center;
  gap: 1.2rem;
  margin-top: 1.5rem;
}

.save-btn,
.cancel-btn {
  flex: 1;
  padding: 0.9rem;
  font-size: 1.1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.save-btn {
  background-color: #4caf50;
  color: #fff;
}

.cancel-btn {
  background-color: #f44336;
  color: #fff;
}

/* =========================
   PC補正
========================= */
@media (min-width: 768px) {
  .modal {
    width: 80%;
  }
}
</style>
