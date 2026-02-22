<template>
  <!-- モーダル背景 -->
  <div class="modal-overlay" @click="$emit('close')">
    <!-- モーダル本体 -->
    <div class="modal" @click.stop>
      <h3 class="modal-title">
        {{ localForm.id ? "習慣を編集" : "新しい習慣を追加" }}
      </h3>

      <form @submit.prevent="save" class="form-body">
        <!-- タイトル -->
        <div class="form-row">
          <label>タイトル</label>
          <input v-model="localForm.title" required />
        </div>

        <!-- 開始 -->
        <div class="form-row">
          <label>開始</label>
          <input type="time" v-model="localForm.start" required />
        </div>

        <!-- 終了 -->
        <div class="form-row">
          <label>終了</label>
          <input type="time" v-model="localForm.end" required />
        </div>

        <!-- 重要度 -->
        <div class="form-row">
          <label>重要度</label>
          <select v-model="localForm.importance">
            <option value="1">★</option>
            <option value="2">★★</option>
            <option value="3">★★★</option>
          </select>
        </div>

        <!-- メモ -->
        <div class="form-row">
          <label>メモ</label>
          <textarea v-model="localForm.memo" rows="4" />
        </div>


        <!-- ボタン -->
        <div class="modal-btns">
          <button type="submit" class="save-btn">保存</button>
          <button type="button" class="cancel-btn" @click="$emit('close')">
            キャンセル
          </button>
        </div>
      </form>
    </div>
  </div>
</template>


<script>
import { ref, watch, toRaw } from "vue";

export default {
  name: "HabitFormModal", // コンポーネント名

  // props: 親から渡されるフォームデータ
  props: {
    formData: { 
      type: Object,   // 編集対象または新規フォーム
      required: true
    }
  },

  // emits: 親に通知するイベント
  emits: ["save", "close"],

  setup(props, { emit }) {
    /**
     * localForm
     * -----------------
     * ローカルで管理するフォームデータ(ref)
     * 目的:
     *   親コンポーネントの formData を直接変更せず、
     *   モーダル内で入力・編集できるようにする
     */
    const localForm = ref({ ...props.formData });

    /**
     * watch
     * -----------------
     * 親から formData が変更された場合に localForm を同期
     * 引数:
     *   () => props.formData : 監視対象
     *   (newVal) => { ... } : 値変更時の処理
     * 処理フロー:
     *   1. props.formData の変更を検知
     *   2. localForm に新しい値をコピー
     * 返り値: なし
     */
    watch(
      () => props.formData,
      (newVal) => {
        localForm.value = { ...newVal };
      }
    );

    /**
     * save
     * -----------------
     * フォーム送信時に呼ばれる関数
     * 役割:
     *   入力された localForm の内容を親コンポーネントに通知
     *   （新規追加・編集両方に対応）
     * 引数: なし（localForm を参照）
     * 処理フロー:
     *   1. toRaw(localForm.value) で reactive/Proxy を解除
     *   2. emit("save", ...) で親に送信
     * 返り値: なし
     */
    function save() {
      emit("save", { ...toRaw(localForm.value) });
    }

    return { localForm, save };
  }
};
</script>

<style scoped>
/* =========================
   背景
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
  background-color: #fff;
  border-radius: 12px;
  padding: 1.8rem;
  width: 70vw;          /* スマホ */
  max-width: 600px;    /* PC最大 */
  font-size: 1.1rem;
}

/* タイトル */
.modal-title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
}

/* =========================
   フォーム
========================= */
.form-body {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

/* 1行ずつ */
.form-row {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
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
.modal-btns {
  margin-top: 1.6rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.modal-btns button {
  flex: 1;                 /* 均等配置 */
  padding: 0.9rem;
  font-size: 1.1rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
}

.save-btn {
  background-color: #1976d2;
  color: #fff;
}

.cancel-btn {
  background-color: #9e9e9e;
  color: #fff;
}

/* =========================
   PCサイズ
========================= */
@media (min-width: 768px) {
  .modal {
    width: 70vw;           /* PC画面の80% */
    font-size: 1.15rem;
  }

  .modal-title {
    font-size: 2rem;
  }
}
</style>
