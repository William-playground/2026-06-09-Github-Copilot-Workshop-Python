# データモデル

## 概要

現在の実装では、データベースは使用していません。タイマーの状態はブラウザ側の JavaScript オブジェクト（インメモリ）で管理されます。

---

## タイマー状態オブジェクト（`state`）

`static/js/app.js` 内で定義されるアプリケーション状態のオブジェクトです。

````javascript
const state = {
    mode: 'work',
    durationSeconds: workSeconds,   // 例: 1500（25分 × 60秒）
    remainingSeconds: workSeconds,
    isRunning: false,
    completedCount: 0,
    focusSeconds: 0,
    intervalId: null,
};
````

### プロパティ一覧

| プロパティ | 型 | 初期値 | 説明 |
|------------|----|--------|------|
| `mode` | `string` | `'work'` | 現在のモード。現状は `'work'` のみ。将来的に `'break'` を追加予定。 |
| `durationSeconds` | `number` | `1500`（25分） | 現在のセッション全体の秒数。`window.POMODORO_CONFIG.workMinutes × 60` で算出。 |
| `remainingSeconds` | `number` | `1500` | 残り秒数。タイマー実行中は 1 秒ごとに減少。 |
| `isRunning` | `boolean` | `false` | タイマーが実行中かどうか。 |
| `completedCount` | `number` | `0` | 今日完了したポモドーロセッションの回数。 |
| `focusSeconds` | `number` | `0` | 今日の累計集中時間（秒）。セッション完了時に `durationSeconds` が加算される。 |
| `intervalId` | `number \| null` | `null` | `setInterval` の ID。タイマー停止時は `null`。 |

---

## 初期設定オブジェクト（`window.POMODORO_CONFIG`）

Flask テンプレートからフロントエンドへ渡される設定値です。`index.html` の `<script>` ブロックで定義されます。

````javascript
window.POMODORO_CONFIG = {
    workMinutes: 25,    // Flask の work_minutes から注入
    breakMinutes: 5,    // Flask の break_minutes から注入（現在未使用）
};
````

| プロパティ | 型 | 値 | 説明 |
|------------|----|----|------|
| `workMinutes` | `number` | `25` | 作業セッションの時間（分）。`state.durationSeconds` の算出に使用。 |
| `breakMinutes` | `number` | `5` | 休憩セッションの時間（分）。現在の実装では参照されていない。 |

---

## 将来的なデータモデル（未実装）

将来的に localStorage や Flask API を追加する際に想定されているデータ構造です。

### localStorage（進捗の永続化）

````text
pomodoro.completedCount     今日の完了回数（数値）
pomodoro.focusSeconds       今日の累計集中秒数（数値）
pomodoro.lastUpdatedDate    最終更新日（YYYY-MM-DD 形式の文字列）
````

`pomodoro.lastUpdatedDate` を参照し、日付が変わっていた場合は完了数と集中時間をリセットします。

### Flask API 用データモデル（SQLite 想定）

````text
sessions テーブル:
  id              INTEGER PRIMARY KEY
  date            TEXT        (YYYY-MM-DD)
  completed_count INTEGER
  focus_seconds   INTEGER
  created_at      TEXT        (ISO 8601 形式)
````
