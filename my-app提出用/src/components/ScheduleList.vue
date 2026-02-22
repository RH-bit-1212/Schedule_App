<template>
  <!-- ★ スクロール用ラッパー -->
  <div class="hour-list-wrapper">
    <div class="hour-list">
      <div
        v-for="hour in hours"
        :key="hour"
        class="hour-row"
      >
        <!-- 時刻 -->
        <div class="hour-label">
          {{ String(hour).padStart(2, "0") }}:00
        </div>

        <!-- タスク枠 -->
        <div class="hour-tasks">
          <div
            v-for="task in tasksByHour(hour)"
            :key="task.id"
            class="task-chip"
            :style="{ backgroundColor: task.color }"
            @click="$emit('row-click', task)"
          >
            {{ task.start }}–{{ task.end }} {{ task.title }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ScheduleHourList",
  props: {
    tasks: {
      type: Array,
      required: true
    }
  },
  computed: {
    hours() {
      return Array.from({ length: 24 }, (_, i) => i);
    },
    coloredTasks() {
      const palette=["#1976d2","#f57c00","#388e3c","#7b1fa2","#fbc02d","#455a64","#c2185b","#00796b","#e64a19","#512da8","#689f38","#5d4037","#0288d1","#d32f2f","#303f9f","#c0ca33","#af5b7d","#0288d1","#388e3c","#1976d2"];



      return this.tasks.map((t, i) => ({
        ...t,
        startMin: this.toMin(t.start),
        endMin: this.toMin(t.end),
        color: palette[i % palette.length]
      }));
    }
  },
  methods: {
    toMin(time) {
      const [h, m] = time.split(":").map(Number);
      return h * 60 + m;
    },
    tasksByHour(hour) {
      const start = hour * 60;
      const end = start + 60;
      return this.coloredTasks.filter(
        t => t.startMin < end && t.endMin > start
      );
    }
  }
};
</script>

<style scoped>
/* ★ 縦スクロールコンテナ */
.hour-list-wrapper {
  height: calc(100vh - 300px); /* ヘッダー等がある場合を考慮 */
  overflow-y: auto;
  border: 1px solid #ccc;
  background: #fff;
}

.hour-list {
  font-family: sans-serif;
}

/* 1時間行 */
.hour-row {
  display: flex;
  border-bottom: 1px solid #e0e0e0;
  min-height: 48px;
}

/* 時刻 */
.hour-label {
  width: 60px;
  padding: 6px;
  text-align: right;
  font-size: 0.85rem;
  color: #555;
  border-right: 1px solid #ccc;
  box-sizing: border-box;
}

/* タスクエリア */
.hour-tasks {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 6px;
  overflow-x: auto;
}

/* タスク表示 */
.task-chip {
  white-space: nowrap;
  color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
}
.task-chip:hover {
  opacity: 0.85;
}
</style>
