<template>
  <div class="clock-box" :style="clockStyle">
    <span class="clock-box-date">{{ date }}</span><br>
    <span class="clock-box-time">{{ time }}</span>
  </div>
</template>

<script>
/*
  AppClock コンポーネント（時刻・日付をリアルタイム表示）

  ■ 役割・概要
    - 現在の「時刻」「日付」を画面に表示するコンポーネント
    - 1 秒ごとに自動更新
    - 時刻によって背景色（朝・昼・夕方・夜）を自動変更する
    - 親に「現在時刻の文字列」を emit する（"time-changed" イベント）

  ■ emit:
      - "time-changed": 時刻更新のたびに現在時刻を親へ通知

  ■ 使用例:
      <AppClock @time-changed="handleClockUpdate" />
*/

import { ref, onMounted, onBeforeUnmount } from "vue";

export default {
  name: "AppClock", // コンポーネント名
  emits: ["time-changed"],

  setup(props, { emit }) {
    // ------------------------------
    // ■ Reactive 変数
    // ------------------------------

    const time = ref("");        // HH:MM:SS の形式で現在時刻を保存
    const date = ref("");        // YYYY/MM/DD（曜日）の形式で日付を保存
    const clockStyle = ref({});  // 時間帯に応じた背景色と文字色を格納

    // setInterval の ID を保持するための変数
    let timer = null;


    // --------------------------------------------------------
    // ■ updateClock()
    //    現在の時刻・日付を取得し、表示内容と背景色を更新する関数
    //
    // 【引数】なし
    // 【返り値】なし
    //
    // 【主な処理内容】
    //   1. 現在時刻を Date() から取得
    //   2. time（HH:MM:SS）を書き換え
    //   3. date（YYYY/MM/DD（曜日））を書き換え
    //   4. "time-changed" イベントで親へ現在時刻を通知
    //   5. 時間帯によって背景色を変更
    // --------------------------------------------------------
    function updateClock() {
      const now = new Date();

      const hours = now.getHours();
      const minutes = String(now.getMinutes()).padStart(2, "0");
      const seconds = String(now.getSeconds()).padStart(2, "0");

      const dayNames = ["日", "月", "火", "水", "木", "金", "土"];

      // 時刻表示（例: 09:32:15）
      time.value = `${String(hours).padStart(2, "0")}:${minutes}:${seconds}`;

      // 日付表示（例: 2025/11/29（土））
      date.value = `${now.getFullYear()}/${now.getMonth() + 1}/${now.getDate()}（${dayNames[now.getDay()]}）`;

      // 親へ "time-changed" イベントを emit
      emit("time-changed", time.value);


      // -------------------------------------------
      // ■ 時間帯ごとに背景色を変更
      //    - 朝    5:00〜11:59
      //    - 昼   12:00〜16:59
      //    - 夕方 17:00〜18:59
      //    - 夜    19:00〜4:59
      // -------------------------------------------
      if (hours >= 5 && hours < 12) {
        // 朝
        clockStyle.value = {
          backgroundColor: "#FFF3C4",
          color: "#333"
        };
      } else if (hours >= 12 && hours < 17) {
        // 昼
        clockStyle.value = {
          backgroundColor: "#4FC3F7",
          color: "#ffffff"
        };
      } else if (hours >= 17 && hours < 19) {
        // 夕方
        clockStyle.value = {
          backgroundColor: "#FFB74D",
          color: "#3E2723"
        };
      } else {
        // 夜
        clockStyle.value = {
          backgroundColor: "#1A237E",
          color: "#ffffff"
        };
      }
    }


    // --------------------------------------------------------
    // ■ ライフサイクルフック
    // --------------------------------------------------------

    // コンポーネントが表示されたときに初期化
    onMounted(() => {
      updateClock();                 // 最初に即時実行
      timer = setInterval(updateClock, 1000); // 1 秒ごとに更新
    });

    // コンポーネントが破棄される前にタイマーを解除
    onBeforeUnmount(() => {
      if (timer) clearInterval(timer);
    });


    // テンプレートに渡す値
    return { time, date, clockStyle };
  }
};
</script>

<style scoped>
.clock-box {
  padding: 12px;
  border-radius: 8px;
  text-align: center;
}

/* 日付 */
.clock-box-date {
  font-size: 40px;
  opacity: 0.8;
}

/* 時刻 */
.clock-box-time {
  font-size: 80px;
  font-weight: 700;
  line-height: 1.2;
}

/* PC・大画面対応 */
@media (min-width: 1024px) {
  .clock-box-date {
    font-size: 40px;
  }

  .clock-box-time {
    font-size: 80px;
  }
}
</style>