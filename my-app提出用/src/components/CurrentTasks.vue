<template>
  <div>
    <!-- タスクが存在する場合の表示 -->
    <div v-if="tasks.length" class="current-tasks-a">
      <h3>【現在の予定】</h3>

      <!-- タスク一覧 -->
      <div
        v-for="task in tasks"
        :key="task.id"
        class="task-item-a"
        :class="[
          `importance-${task.importance}`,
          { expanded: expandedTaskId === task.id }
        ]"
        @click="toggleTask(task.id)"
      >
        <!-- タイトル -->
        <div class="task-title-a">
          {{ task.title }} ({{ task.type }})
        </div>

        <hr class="task-divider" />

        <!-- メモ（省略／全文切替） -->
        <div class="task-detail-a memo">
          <strong>メモ：</strong>
          <span>{{ task.memo || "ー" }}</span>
        </div>

        <div class="task-detail-a">
          <strong>時間：</strong>{{ task.start }} ~ {{ task.end }}
        </div>

        <div class="task-detail-a">
          <strong>重要度：</strong>{{ "★".repeat(task.importance) }}
        </div>

        <!-- 完了チェック（クリック伝播防止） -->
        <div class="task-detail-a" @click.stop>
          <label>
            完了:
            <input
              type="checkbox"
              v-model="task.done"
              @change="emitUpdate(task)"
            />
          </label>
        </div>
      </div>
    </div>

    <!-- タスクが存在しない場合 -->
    <div v-else>
      現在進行中のタスクはありません
    </div>
  </div>
</template>


<script>
import { ref } from "vue";

export default {
  name: "CurrentTasks",
  
  // props：親コンポーネントから渡される値
  props: {
    tasks: {
      type: Array, // タスクの配列
      required: true // 必須
    }
  },

  // emits：子から親へ通知するイベント
  emits: ["update-done"],

  setup(props, { emit }) {
    /**
     * emitUpdate
     * ---------------
     * 役割: タスクの完了状態が変更された際に、親コンポーネントに通知する
     * 引数: 
     *   task (Object) - 完了状態が変更されたタスクオブジェクト
     * 処理:
     *   1. emit 関数を使って 'update-done' イベントを親に送信
     * 返り値: なし
     */
    const expandedTaskId = ref(null);

    function toggleTask(id) {
      expandedTaskId.value =
        expandedTaskId.value === id ? null : id;
    }

    function emitUpdate(task) {
      emit("update-done", task);
    }

    return {
      emitUpdate,
      expandedTaskId,
      toggleTask
    };
  }
};
</script>

<style scoped>

/* =========================
   コンポーネント全体
========================= */
.current-tasks-a {
  margin: 10px 0;
}

/* スマホ：カード間に余白 */
.task-item-a {
  margin-bottom: 10px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #f9f9f9;
  cursor: pointer;
}

/* =========================
   タイトル
========================= */
.task-title-a {
  font-weight: bold;
  font-size: 20px;
}

/* 区切り線 */
.task-divider {
  margin: 6px 0;
  border: none;
  border-top: 1px solid #ddd;
}

/* 詳細行 */
.task-detail-a {
  margin: 4px 0;
  font-size: 16px;
}


/* =========================
   メモ表示（改行・空白対応）
========================= */
.task-detail-a.memo span {
  display: -webkit-box;
  -webkit-line-clamp: 1;        /* 通常は2行まで */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;

  white-space: pre-wrap;       /* ← 改行・空白を保持 */
  word-break: break-word;      /* 長文折り返し */
}

/* 展開時は全文表示 */
.task-item-a.expanded .task-detail-a.memo span {
  display: block;
  -webkit-line-clamp: unset;
  overflow: visible;

  white-space: pre-wrap;       /* 改行・空白そのまま */
}


/* =========================
   重要度別カラー
========================= */
.importance-1 {
  background-color: #E3F2FD;
  border-color: #90CAF9;
}

.importance-2 {
  background-color: #FFF9C4;
  border-color: #FFF176;
}

.importance-3 {
  background-color: #FFEBEE;
  border-color: #EF9A9A;
}

/* =========================
   PC：Grid化
========================= */
@media (min-width: 768px) {
  .current-tasks-a {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 12px;
  }

  .current-tasks-a > h3 {
    grid-column: 1 / -1;
  }

  .task-item-a {
    margin-bottom: 0; /* Grid gap に任せる */
  }
}

/* =========================
   PC操作向け
========================= */
@media (hover: hover) {
  .task-item-a:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }
}

</style>
