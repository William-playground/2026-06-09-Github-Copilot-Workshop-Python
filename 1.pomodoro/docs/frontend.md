# フロントエンドドキュメント

## 概要

フロントエンドは HTML テンプレート、CSS スタイルシート、JavaScript の 3 ファイルで構成されています。すべてのタイマーロジックと DOM 操作は `static/js/app.js` 単一ファイルに実装されています。

---

## ファイル構成

| ファイル | 役割 |
|----------|------|
| `templates/index.html` | アプリの HTML 構造とサーバー設定の受け渡し |
| `static/css/style.css` | UI スタイリング |
| `static/js/app.js` | タイマーロジック、DOM 更新、イベント処理 |

---

## HTML テンプレート（`index.html`）

### 画面構造

````text
body
  .app-shell              最大幅 500px の中央配置コンテナ
    .window               ウィンドウカード（角丸、シャドウ）
      .titlebar           タイトルバー（タイトル + 操作ボタン）
      .status-label       ステータス表示（「作業中」「停止中」）
      .timer-ring-container  円形タイマー領域
        svg.timer-ring    SVG リング（背景 + プログレス）
        .timer-display    タイマー数値表示（MM:SS）
      .actions            操作ボタン（開始/一時停止、リセット）
      .daily-summary      今日の進捗（完了回数、集中時間）
````

### 主要な DOM 要素

| ID | 要素 | 説明 |
|----|------|------|
| `#timer-text` | `<span>` | 残り時間（MM:SS 形式）を表示 |
| `#status-text` | `<span>` | 現在のステータスを表示 |
| `#start-btn` | `<button>` | 開始/一時停止ボタン |
| `#reset-btn` | `<button>` | リセットボタン |
| `#progress-ring` | `<circle>` | SVG 進捗リング |
| `#completed-count` | `<div>` | 今日の完了回数を表示 |
| `#focus-hours` | `<div>` | 今日の集中時間を表示（例: `0時間25分`） |

### サーバー設定の受け渡し

Flask から渡された初期設定を `window.POMODORO_CONFIG` に格納します。

````html
<script>
    window.POMODORO_CONFIG = {
        workMinutes: {{ work_minutes | tojson }},
        breakMinutes: {{ break_minutes | tojson }},
    };
</script>
````

---

## CSS（`style.css`）

### 主要なクラス

| クラス | 説明 |
|--------|------|
| `.app-shell` | アプリ全体のラッパー。`max-width: 500px`、中央配置。 |
| `.window` | ウィンドウカード。`background: #f5f5f7`、`border-radius: 16px`。 |
| `.titlebar` | タイトルバー。白背景、高さ 50px。 |
| `.titlebar-btn` | タイトルバーのアイコンボタン（最小化・最大化・閉じる）。 |
| `.titlebar-btn.close:hover` | 閉じるボタンのホバー時に赤背景（`#ff5f57`）。 |
| `.timer-ring` | SVG タイマーリング。220×220px、`transform: rotate(-90deg)` で開始位置を上部に。 |
| `.timer-ring-bg` | SVG 背景リング。`stroke: #e8e8e8`、`stroke-width: 12`。 |
| `.timer-ring-progress` | SVG 進捗リング。`stroke: #667eea`、`stroke-dasharray: 565.48`（2π×90）。 |
| `.timer-display` | タイマー数値表示。フォント `Monaco/Courier New`、56px、太字。 |
| `.btn-primary` | 開始ボタン。紫グラデーション背景（`#667eea` → `#764ba2`）。 |
| `.btn-secondary` | リセットボタン。白背景、紫ボーダー。 |
| `.daily-summary` | 今日の進捗。2 列グリッドレイアウト。 |

### レスポンシブ対応

`@media (max-width: 480px)` で小画面向けの調整を行っています。

- タイマーフォントサイズ: 56px → 48px
- リングサイズ: 220px → 180px
- ボタンパディング縮小

---

## JavaScript（`app.js`）

### 関数一覧

#### `formatTime(seconds)`

秒数を `MM:SS` 形式の文字列に変換します。

````javascript
formatTime(1500) // → "25:00"
formatTime(65)   // → "01:05"
````

| 引数 | 型 | 説明 |
|------|----|------|
| `seconds` | `number` | 変換する秒数 |

**戻り値**: `string`（`MM:SS` 形式）

---

#### `updateUI()`

現在の `state` を参照して、すべての DOM 要素を更新します。

- `#timer-text` に残り時間（`formatTime(state.remainingSeconds)`）を設定
- `#status-text` を `state.isRunning` に応じて「作業中」または「停止中」に設定
- `#start-btn` のテキストを「開始」または「一時停止」に切り替え
- `#completed-count` に `state.completedCount` を設定
- `#focus-hours` に集中時間（`X時間Y分` 形式）を設定
- `#progress-ring` の `strokeDashoffset` を進捗に応じて更新

**進捗リングの計算式**:
````javascript
const progress = (state.durationSeconds - state.remainingSeconds) / state.durationSeconds;
const circumference = 2 * Math.PI * 90; // r = 90 → 565.48...
const offset = circumference * (1 - progress);
progressRing.style.strokeDashoffset = offset;
````

---

#### `startTimer()`

開始ボタンクリック時に呼び出されます。現在の `state.isRunning` に応じて動作が異なります。

**開始時（`state.isRunning === false`）**:
- `state.isRunning = true` に設定
- `setInterval` で 1 秒ごとに `state.remainingSeconds` を 1 減算
- `remainingSeconds` が 0 になるとセッション完了処理を行う

**一時停止時（`state.isRunning === true`）**:
- `state.isRunning = false` に設定
- `clearInterval` でタイマーを停止

**セッション完了時**:
- `state.completedCount += 1`
- `state.focusSeconds += state.durationSeconds`
- `state.remainingSeconds` をリセット
- `alert()` で「セッション完了！休憩しましょう。」を通知

---

#### `resetTimer()`

リセットボタンクリック時に呼び出されます。

- タイマーを停止（`clearInterval`）
- `state.isRunning = false`
- `state.remainingSeconds = state.durationSeconds`（初期値に戻す）
- `updateUI()` を呼び出して表示を更新

---

### イベントリスナー

````javascript
startBtn.addEventListener('click', startTimer);
resetBtn.addEventListener('click', resetTimer);
````

---

### 初期化フロー

1. `window.POMODORO_CONFIG` から `workMinutes` を読み込む（未定義時はデフォルト `25`）
2. `workSeconds = workMinutes * 60` を計算
3. `state` オブジェクトを初期化
4. `updateUI()` を呼び出して初期表示を設定

---

## 未実装の予定機能

当初の設計で計画されていたが、現時点では未実装のフロントエンド機能です。

| 機能 | ファイル | 説明 |
|------|----------|------|
| タイマーロジックの分離 | `timer-core.js` | 純粋関数によるタイマー状態管理（DOM 非依存） |
| DOM 更新の分離 | `timer-ui.js` | DOM 操作の専用モジュール |
| 進捗の永続化 | `storage.js` | localStorage への進捗保存・復元・日付リセット |
| JavaScript テスト | `tests/js/timer-core.test.js` | Vitest によるユニットテスト |
