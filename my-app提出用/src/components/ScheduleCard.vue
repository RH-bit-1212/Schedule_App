<template>
  <!-- スクロール専用ラッパー -->
  <div class="card-scroll-area">
    <div class="card-wrapper">
      <div
        v-for="task in tasks"
        :key="task.id"
        class="task-card"
        :class="task.type === 'スケジュール' ? 'schedule-card' : 'habit-card'"
        @click="$emit('row-click', task)"
      >
        <!-- タイトル -->
        <h4 class="title">{{ task.title }}</h4>

        <!-- 種類・時間 -->
        <div class="meta">
          <span class="type">{{ task.type }}</span>
          <span class="time">{{ task.start }} ~ {{ task.end }}</span>
        </div>

        <!-- 重要度 -->
        <div class="importance">
          <span
            v-for="n in task.importance"
            :key="n"
            class="star"
          >★</span>
        </div>

        <!-- メモ（あれば表示） -->
        <p v-if="task.memo" class="memo">
          {{ task.memo }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ScheduleCard",
  props: {
    tasks: {
      type: Array,
      required: true
    }
  }
};
</script>

<style scoped>
/* ===== スクロール領域 ===== */
.card-scroll-area {
  max-height: calc(100vh - 300px); /* ヘッダ・フィルタ等を考慮 */
  overflow-y: auto;
  padding-right: 4px; /* スクロールバー余白 */
}

/* ===== カード一覧 ===== */
.card-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

/* ===== カード ===== */
.task-card {
  padding: 14px;
  border-radius: 10px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  transition: transform 0.1s, box-shadow 0.1s;
}
.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.12);
}

/* 種類別 */
.schedule-card {
  background: #e3f2fd;
}
.habit-card {
  background: #fff3e0;
}

/* ===== 中身 ===== */
.title {
  margin: 0 0 6px;
  font-size: 1rem;
}

.meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #555;
  margin-bottom: 6px;
}

.type {
  font-weight: bold;
}

.time {
  white-space: nowrap;
}

/* 重要度 */
.importance {
  color: #f57c00;
  font-size: 0.9rem;
  margin-bottom: 6px;
}

/* メモ */
.memo {
  font-size: 0.8rem;
  color: #444;
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style>
