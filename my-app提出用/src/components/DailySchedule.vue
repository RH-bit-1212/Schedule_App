<template>
  <div class="all-tasks" v-if="tasks.length">
    <!-- タイトル -->
    <h4 class="all-tasks-title">【今日の予定】</h4>

    <!-- ナビゲーション行 -->
    <div class="task-nav">
      <!-- 前へ -->
      <button
        class="nav-btn left"
        @click="emitPrev"
        :disabled="viewIndex === 0"
      >
        ◀
      </button>

      <!-- タスク表示 -->
      <div class="task-content">
        <div class="task-time">
          {{ tasks[viewIndex].start }} ~ {{ tasks[viewIndex].end }}
        </div>
        <div class="task-title">
          {{ tasks[viewIndex].title }} ({{ tasks[viewIndex].type }})
        </div>
      </div>

      <!-- 次へ -->
      <button
        class="nav-btn right"
        @click="emitNext"
        :disabled="viewIndex === tasks.length - 1"
      >
        ▶
      </button>
    </div>
  </div>
</template>


<script>
export default {
  name: "DailySchedule", // コンポーネント名

  // props：親コンポーネントから渡されるデータ
  props: {
    tasks: {
      type: Array, // タスクオブジェクトの配列
      required: true // 必須
    },
    viewIndex: {
      type: Number,  // 現在表示中のタスクのインデックス
      required: true
    }
  },

  // emits：子コンポーネントから親に通知するイベント
  emits: ["prev", "next"],

  methods: {
    /**
     * emitPrev
     * -----------------
     * 役割：
     *   前タスクボタンをクリックした際に親コンポーネントに通知する
     * 引数：
     *   なし
     * 処理フロー：
     *   1. this.$emit を使って "prev" イベントを親に送信
     * 返り値：
     *   なし
     */
    emitPrev() {
      this.$emit("prev");
    },

    /**
     * emitNext
     * -----------------
     * 役割：
     *   次タスクボタンをクリックした際に親コンポーネントに通知する
     * 引数：
     *   なし
     * 処理フロー：
     *   1. this.$emit を使って "next" イベントを親に送信
     * 返り値：
     *   なし
     */
    emitNext() {
      this.$emit("next");
    }
  }
};
</script>

<style scoped>
/* =========================
   全体
========================= */
.all-tasks {
  margin: 10px 0;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f2f2f2;
}

/* =========================
   タイトル中央揃え
========================= */
.all-tasks-title {
  text-align: center;
  font-weight: bold;
  margin-bottom: 8px;
}

/* =========================
   ナビゲーション行
========================= */
.task-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* =========================
   左右ボタン
========================= */
.nav-btn {
  width: 36px;
  height: 36px;
  font-size: 16px;
  border: none;
  border-radius: 50%;
  background-color: #68dfd9ff;
  cursor: pointer;
}

.nav-btn:disabled {
  opacity: 0.4;
  cursor: default;
}

/* =========================
   タスク内容（中央）
========================= */
.task-content {
  flex: 1;
  text-align: center;
  padding: 0 8px;
}

/* 時間 */
.task-time {
  font-size: 13px;
  color: #555;
}

/* タスク名中央揃え */
.task-title {
  font-size: 15px;
  font-weight: 600;
  margin-top: 2px;
  text-align: center;
}

/* =========================
   PC向け微調整
========================= */
@media (min-width: 768px) {
  .task-title {
    font-size: 16px;
  }
}
</style>
