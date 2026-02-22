// src/api/api.js

export const API_URL = "http://localhost:8000";    // FastAPI の URL
// export const API_URL = "http://localhost:3000";   // json-server の URL
// export const API_URL = "http://localhost:8001";    // Mongo の URL

/**
 * 共通レスポンスハンドラ
 */
async function handleResponse(res) {
    // 正常系
    if (res.ok) {
        // DELETE など body が空の可能性を考慮
        const text = await res.text();
        return text ? JSON.parse(text) : null;
    }

    // エラー系
    let errorDetail = null;
    try {
        errorDetail = await res.json();
    } catch {
        errorDetail = null;
    }

    const error = new Error();
    error.status = res.status;

    switch (res.status) {
        case 422:
            error.message = "入力内容が不正です";
            error.detail = errorDetail?.detail ?? null;
            break;

        case 404:
            error.message = "対象データが見つかりません";
            break;

        default:
            error.message = `サーバーエラー (${res.status})`;
            break;
    }

    throw error;
}

// -----------------------------
// 一覧取得（GET /tasks）
// -----------------------------
export async function fetchTasks() {
    const res = await fetch(`${API_URL}/tasks`);
    return handleResponse(res);
}

// -----------------------------
// 新規作成（POST /tasks）
// -----------------------------
export async function addTask(payload) {
    const res = await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    return handleResponse(res);
}

// -----------------------------
// 詳細取得（GET /tasks/{id}）
// -----------------------------
export async function fetchTask(id) {
    const res = await fetch(`${API_URL}/tasks/${id}`);
    return handleResponse(res);
}

// -----------------------------
// 更新（PUT /tasks/{id}）
// -----------------------------
export async function updateTask(id, payload) {
    const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    return handleResponse(res);
}

// -----------------------------
// 削除（DELETE /tasks/{id}）
// -----------------------------
export async function deleteTask(id) {
    const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE",
    });
    return handleResponse(res);
}