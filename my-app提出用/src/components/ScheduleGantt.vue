<template>
  <div class="gantt-root">
    <!-- ===== ヘッダ ===== -->
    <div class="gantt-header">
      <div class="name-col header-cell">名前 / 項目</div>
      <div class="time-header" ref="headerTime">
        <div class="time-cell" v-for="h in 24" :key="h">
          {{ String(h - 1).padStart(2, "0") }}
        </div>
      </div>
    </div>

    <!-- ===== ボディ ===== -->
    <div class="gantt-body">
      <!-- 左列：タスク名 -->
      <div class="name-col" ref="nameCol">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="task-name"
          @click="$emit('row-click', task)"
        >
          {{ task.title }}
        </div>
      </div>

      <!-- 右列：タイムライン -->
      <div class="body-scroll" ref="bodyScroll" @scroll="syncScroll">
        <div class="timeline">
          <div class="task-row" v-for="task in computedTasks" :key="task.id">
            <div
              class="task-bar"
              :style="task.style"
              @click.stop="$emit('row-click', task)"
            >
              {{ task.start }}-{{ task.end }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ScheduleGantt",
  props: {
    tasks: { type: Array, required: true }
  },
  computed: {
    computedTasks() {
      const colors=["#1976d2","#f57c00","#388e3c","#7b1fa2","#fbc02d","#455a64","#c2185b","#00796b","#e64a19","#512da8","#689f38","#5d4037","#0288d1","#d32f2f","#303f9f","#c0ca33","#af5b7d","#0288d1","#388e3c","#1976d2"];

      return this.tasks.map((t, i) => {
        const startMin = this.toMin(t.start);
        const endMin = this.toMin(t.end);
        return {
          ...t,
          style: {
            left: `${startMin}px`,
            width: `${endMin - startMin}px`,
            backgroundColor: colors[i % colors.length]
          }
        };
      });
    }
  },
  methods: {
    toMin(time) {
      const [h, m] = time.split(":").map(Number);
      return h * 60 + m;
    },
    syncScroll() {
      const body = this.$refs.bodyScroll;
      if (!body) return;
      // 横スクロールはヘッダと同期
      if (this.$refs.headerTime) this.$refs.headerTime.scrollLeft = body.scrollLeft;
      // 縦スクロールは左列と同期
      if (this.$refs.nameCol) this.$refs.nameCol.scrollTop = body.scrollTop;
    }
  }
};
</script>

<style scoped>
.gantt-root { border: 1px solid #ccc; font-size: 14px; }

/* ===== ヘッダ ===== */
.gantt-header { display: flex; border-bottom: 1px solid #ccc; background: #f5f5f5; }
.header-cell { font-weight: bold; width: 200px; flex-shrink: 0; }
.time-header { display: grid; grid-template-columns: repeat(24, 60px); height: 48px; overflow-x: hidden; }
.time-cell { text-align: center; line-height: 48px; border-left: 1px solid #ddd; }

/* ===== ボディ ===== */
.gantt-body { display: flex; height: calc(100vh - 350px); overflow: hidden; }
.name-col { width: 100px; border-right: 1px solid #ccc; flex-shrink: 0; overflow: hidden; }
.task-name { height: 48px; line-height: 48px; padding: 0 8px; border-bottom: 1px solid #eee; cursor: pointer; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ===== タイムライン ===== */
.body-scroll { flex: 1; overflow: auto; }
.timeline { width: calc(24 * 60px); }
.task-row { position: relative; height: 48px; border-bottom: 1px solid #eee; background-image: repeating-linear-gradient(to right,#f8f8f8 0,#f8f8f8 59px,#e0e0e0 60px); }
.task-bar { position: absolute; top: 8px; height: 32px; padding: 4px 6px; border-radius: 4px; color: #fff; font-size: 12px; cursor: pointer; white-space: nowrap; }
.task-bar:hover { opacity: 0.85; }
</style>
