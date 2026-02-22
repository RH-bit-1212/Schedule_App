<template>
  <!-- モーダル背景（クリックで閉じる） -->
  <div class="modal-overlay" @click="$emit('close')">
    <!-- モーダル本体 -->
    <div class="modal" @click.stop>
      <!-- タイトル -->
      <h3 class="modal-title">詳細表示</h3>

      <!-- 内容 -->
      <div class="modal-content">
        <p class="item">
          <span class="label">タイトル：</span>
          <span class="value">{{ habit.title }}</span>
        </p>

        <p class="item">
          <span class="label">時間：</span>
          <span class="value">{{ habit.start }} ~ {{ habit.end }}</span>
        </p>

        <p class="item">
          <span class="label">重要度：</span>
          <span class="value stars">
            {{ '★'.repeat(habit.importance) }}
          </span>
        </p>

        <!-- メモ（長文対応） -->
        <div class="item memo">
          <span class="label">メモ：</span>
          <div class="memo-box">
           {{ habit.memo || 'ー' }}
         </div>
        </div>
      </div>



      <!-- 完了チェック（閉じるボタン直上・中央寄せ） -->
      <div class="modal-footer">
        <label class="done-checkbox">
          <input
            type="checkbox"
            v-model="localDone"
            @change="updateDone"
          />
          <span class="done-text">
            {{ localDone ? '✔ 完了' : '未完了' }}
          </span>
        </label>

        <!-- 閉じるボタン -->
        <button class="close-btn" @click="$emit('close')">
          閉じる
        </button>
      </div>
    </div>
  </div>
</template>


<script>
import { ref, watch } from "vue";

export default {
  name: "HabitDetailModal", // コンポーネント名

  // props: 親コンポーネントから受け取るデータ
  props: {
    habit: { 
      type: Object,   // 習慣・タスクの情報
      required: true  // 必須
    }
  },

  // emits: 親に通知するイベント
  emits: ["close", "update-done"],

  setup(props, { emit }) {
    /**
     * localDone
     * -----------------
     * ローカルな完了状態を保持する ref
     * 初期値は親から渡された habit.done
     */
    const localDone = ref(props.habit.done);

    /**
     * watch
     * -----------------
     * 親コンポーネントで habit.done が更新された場合に
     * localDone を同期する
     * 引数:
     *   () => props.habit.done : 監視対象
     *   (newVal) => { ... } : 値変更時のコールバック
     * 処理フロー:
     *   1. habit.done の変更を検知
     *   2. localDone.value に新しい値を設定
     * 返り値: なし
     */
    watch(
      () => props.habit.done,
      (newVal) => {
        localDone.value = newVal;
      }
    );

    /**
     * updateDone
     * -----------------
     * 完了状態チェックボックス変更時に呼び出される関数
     * 役割:
     *   親コンポーネントに更新情報を通知
     * 引数: なし（localDone を参照）
     * 処理フロー:
     *   1. habit の情報をスプレッドでコピー
     *   2. done プロパティに localDone.value を設定
     *   3. emit("update-done", ...) で親に通知
     * 返り値: なし
     */
    function updateDone() {
      emit("update-done", { ...props.habit, done: localDone.value });
    }

    return { localDone, updateDone };
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
  background-color: #fff;
  border-radius: 12px;
  padding: 1.8rem;
  width: 70vw;
  height: 50vh;
  max-width: 600px;
  max-height: 700px;
  display: flex;
  flex-direction: column;
  font-size: 1.05rem;
}

/* =========================
   タイトル
========================= */
.modal-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

/* =========================
   情報表示エリア
========================= */
.modal-content {
  flex: 1;
  overflow-y: auto;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 1.6rem;   /* 高さの余白を広めに */
  text-align: center;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

/* ラベル */
.label {
  font-size: 1.3rem;
  font-weight: 700;
  color: #555;
}

/* 値 */
.value {
  font-size: 1.25rem;
}

/* 重要度 */
.stars {
  font-size: 1.4rem;
  color: #f57c00;
  letter-spacing: 2px;
}

/* =========================
   メモ（長文対応）
========================= */
.memo {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.memo-box {
  font-size: 1.1rem;
  padding: 0.8rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  max-height: 150px;
  overflow-y: auto;
  white-space: pre-wrap;
}


/* =========================
   フッター（完了＋閉じる）
========================= */
.modal-footer {
  display: flex;
  flex-direction: column;
  align-items: center; /* 左右中央ぞろえ */
  gap: 2.0rem;
  margin-top: 1rem;
}

/* 完了チェック */
.done-checkbox {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  cursor: pointer;
}

.done-checkbox input[type="checkbox"] {
  transform: scale(1.8);
}

.done-text {
  font-size: 1.8rem;
  font-weight: 700;
}

/* =========================
   閉じるボタン
========================= */
.close-btn {
  padding: 0.8rem 1.6rem;
  font-size: 1.1rem;
  border-radius: 8px;
  border: none;
  background-color: #1976d2;
  color: #fff;
  cursor: pointer;
}

/* =========================
   PCサイズ補正
========================= */
@media (min-width: 768px) {
  .modal {
    width: 60vw;
    height: 60vh;
    font-size: 1.15rem;
  }

  .modal-title {
    font-size: 1.6rem;
  }

  .label {
    font-size: 1.35rem;
  }

  .value {
    font-size: 1.25rem;
  }

  .done-text {
    font-size: 1.4rem;
  }
}
</style>
