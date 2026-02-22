
/*
==================================================
【概要】
Vue Router のルーティング定義ファイル。
・画面遷移ルールの一元管理
・URL とコンポーネントの対応付け
・モーダル表示（詳細／編集）を URL で制御
を担当する。

【設計方針】
・一覧画面（/habits, /schedules）を基点とする
・詳細／編集は :id を含む URL で直接アクセス可能
・不正 URL はトップへリダイレクト
==================================================
*/

import { createRouter, createWebHistory } from "vue-router";

const MainView = () => import("../components/MainView.vue");

const HabitTrackerView = () => import("../components/HabitTrackerView.vue");
const HabitDetailModal = () => import("../components/HabitDetailModal.vue");
const HabitFormModal   = () => import("../components/HabitFormModal.vue");

const ScheduleView = () => import("../components/ScheduleView.vue");
const ScheduleDetailModal = () => import("../components/ScheduleDetailModal.vue");
const ScheduleForm = () => import("../components/ScheduleForm.vue");

/*
--------------------------------------------------
【ルーティング定義】
・path      : URL パス
・component : 表示するコンポーネント
・props     : true の場合、:id を props として渡す
--------------------------------------------------
*/
const routes = [
  // ルートアクセスは MainView に
  { path: "/", component: MainView },

  // --- 習慣トラッカー ---
  { path: "/habits", component: HabitTrackerView },
  { path: "/habits/:id", component: HabitDetailModal, props: true },
  { path: "/habits/:id/edit", component: HabitFormModal, props: true },

  // --- スケジュール ---
  { path: "/schedules", component: ScheduleView },
  { path: "/schedules/:id", component: ScheduleDetailModal, props: true },
  { path: "/schedules/:id/edit", component: ScheduleForm, props: true },

  // その他の不正URLは / にリダイレクト
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

/*
--------------------------------------------------
【Router インスタンス生成】
・history: HTML5 History API を使用
・routes : 上記で定義したルーティング
--------------------------------------------------
*/
export default createRouter({
  history: createWebHistory(),
  routes,
});
