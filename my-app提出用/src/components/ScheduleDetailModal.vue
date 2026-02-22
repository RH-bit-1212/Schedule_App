<template>
  <div
    v-if="localTask"
    class="modal-overlay"
    @click="$emit('close')"
  >
    <div class="modal" @click.stop>
      <!-- タイトル -->
      <h3 class="modal-title">詳細表示</h3>

      <!-- 内容 -->
      <div class="modal-content">
        <p class="item">
          <span class="label">タイトル：</span>
          <span class="value">{{ localTask.title }}</span>
        </p>

        <!-- ★ 追加：種類 -->
        <p class="item">
          <span class="label">種類：</span>
          <span class="value">
            {{ localTask.type === 'schedule' ? 'スケジュール' : '習慣' }}
          </span>
      </p>

        <p class="item">
          <span class="label">時間：</span>
          <span class="value">
            {{ localTask.start }} ~ {{ localTask.end }}
          </span>
        </p>

        <p class="item">
          <span class="label">重要度：</span>
          <span class="value stars">
            {{ '★'.repeat(localTask.importance) }}
          </span>
        </p>

        <!-- メモ（長文対応） -->
        <div class="item memo">
          <span class="label">メモ：</span>
          <div class="memo-box">
            {{ localTask.memo || 'ー' }}
          </div>
        </div>
      </div>

      <!-- フッター -->
      <div class="modal-footer">
        <!-- 完了 -->
        <label class="done-checkbox">
          <input
            type="checkbox"
            v-model="localTask.done"
            @change="$emit('update-done', localTask)"
          />
          <span class="done-text">
            {{ localTask.done ? '✔ 完了' : '未完了' }}
          </span>
        </label>

        <!-- 操作ボタン（既存維持） -->
        <div class="button-row">
          <button
            class="edit-btn"
            @click="$emit('edit', localTask)"
          >
            編集
          </button>
          <button
            class="delete-btn"
            @click="$emit('delete', localTask.id, localTask.type)"
          >
            削除
          </button>
          <button class="close-btn" @click="$emit('close')">
            閉じる
          </button>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
export default {
  name: "ScheduleDetailModal",

  /**
   * props
   * -----------------
   * task: Object | null
   *   - 表示対象のタスク（スケジュール/習慣など）
   *   - 省略可能（デフォルト null）
   */
  props: {
    task: {
      type: Object,
      required: false,
      default: null
    }
  },

  /**
   * data
   * -----------------
   * localTask: Object | null
   *   - props.task のコピー。直接 props を変更せずに v-model で編集可能にする
   */
  data() {
    return {
      localTask: null
    };
  },

  /**
   * watch
   * -----------------
   * props.task の変更を監視し localTask にコピー
   * immediate: true で初回マウント時にも handler を実行
   * handler(newVal):
   *   - newVal が存在する場合、スプレッド構文でコピーを作成
   *   - null の場合は localTask も null に設定
   * 引数:
   *   - newVal: 更新された task オブジェクト
   * 処理フロー:
   *   1. task が変更されたらコピーを作成
   *   2. モーダル内の v-model は localTask を参照
   * 返り値: なし
   */
  watch: {
    task: {
      immediate: true,
      handler(newVal) {
        this.localTask = newVal ? { ...newVal } : null;
      }
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
  background-color: #fff;
  border-radius: 12px;
  padding: 1.8rem;
  width: 70vw;
  height: 63vh;
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
  gap: 1.6rem;
  text-align: center;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.label {
  font-size: 1.3rem;
  font-weight: 700;
  color: #555;
}

.value {
  font-size: 1.25rem;
  white-space: pre-wrap;
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
   フッター
========================= */
.modal-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.6rem;
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
   ボタン
========================= */
.button-row {
  display: flex;
  gap: 1rem;
}

button {
  padding: 0.7rem 1.4rem;
  font-size: 1.05rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.edit-btn {
  background-color: #e3f2fd;
}

.delete-btn {
  background-color: #ffebee;
}

.close-btn {
  background-color: #1976d2;
  color: #fff;
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
