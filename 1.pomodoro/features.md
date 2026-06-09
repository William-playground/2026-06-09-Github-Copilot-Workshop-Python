# ポモドーロタイマー - 実装機能一覧

## 初期実装に必要な機能

### 1. Flask アプリケーション
- [ ] アプリファクトリ形式の実装（`create_app()`）
- [ ] GET `/` ルートの実装（HTML テンプレート配信）
- [ ] 初期パラメータの受け渡し（work_minutes=25、break_minutes=5）

### 2. HTML テンプレート（index.html）
- [ ] アプリシェル・ウィンドウ構造の実装
- [ ] タイトルバー表示
- [ ] ステータスラベル表示
- [ ] 円形タイマー表示（SVG または CSS）
- [ ] 操作ボタン（開始、一時停止、リセット）
- [ ] 今日の進捗表示（完了回数、集中時間）

### 3. CSS スタイル（style.css）
- [ ] UI モックに沿った背景とレイアウト
- [ ] ウィンドウカードのスタイリング
- [ ] 円形プログレスリングの実装
- [ ] ボタンのスタイリング（開始、リセット）
- [ ] 進捗表示セクションのスタイリング

### 4. JavaScript コアロジック（timer-core.js）
- [ ] `createInitialState()` - 初期状態生成
- [ ] `startTimer(state)` - タイマー開始
- [ ] `pauseTimer(state)` - タイマー一時停止
- [ ] `resetTimer(state)` - リセット
- [ ] `tick(state)` - 1秒経過時の状態更新
- [ ] `completeSession(state)` - セッション完了処理
- [ ] `formatTime(seconds)` - 秒数を mm:ss 形式に変換
- [ ] `getProgress(state)` - 円形プログレス用の進捗率計算

### 5. JavaScript UI 更新（timer-ui.js）
- [ ] 残り時間の画面反映
- [ ] ステータス表示の更新（「作業中」「停止中」など）
- [ ] 円形プログレスバーの更新
- [ ] ボタン表示状態の管理（開始→一時停止への切り替え）
- [ ] 今日の進捗表示の更新

### 6. JavaScript localStorage 管理（storage.js）
- [ ] `saveProgress()` - 進捗を localStorage に保存
- [ ] `loadProgress()` - 進捗を復元
- [ ] `resetIfNewDay()` - 日付変更時のリセット
- [ ] `pomodoro.completedCount`、`pomodoro.focusSeconds`、`pomodoro.lastUpdatedDate` の管理

### 7. JavaScript メインアプリ（app.js）
- [ ] 各モジュールの初期化
- [ ] イベントリスナー登録（ボタンクリック）
- [ ] `setInterval` でのタイマー実行管理

### 8. Python テスト（test_app.py）
- [ ] `GET /` が 200 を返すテスト
- [ ] テンプレートが正しくレンダリングされるテスト
- [ ] Flask テストクライアントの実装

### 9. JavaScript テスト（tests/js/*.test.js）
- [ ] `timer-core.js` のユニットテスト（Vitest）
  - 開始・一時停止・リセット機能
  - 1秒経過の正確性
  - 完了判定ロジック
  - 時刻フォーマット変換
- [ ] `storage.js` のテスト
  - localStorage 保存・復元
  - 日付変更検出

## 実装順序

1. Flask のアプリファクトリと `/` ルートを作成
2. `templates/index.html` に UI の HTML 構造を作成
3. `static/css/style.css` で UI モックの見た目を再現
4. `static/js/timer-core.js` にタイマーの純粋ロジックを実装
5. `static/js/timer-ui.js` に DOM 更新処理を実装
6. `static/js/storage.js` に localStorage 保存処理を実装
7. `static/js/app.js` でイベント登録と各モジュールの接続を実施
8. `tests/test_app.py` で Flask のルーティングテストを追加
9. `tests/js/timer-core.test.js` でタイマーの状態遷移テストを追加
10. 必要に応じて通知音、ブラウザ通知、休憩モード、履歴 API を追加

## 将来的な拡張案

- [ ] 休憩モード（`mode` に `break` を追加）
- [ ] 長い休憩（4 回完了ごとに長い休憩へ切り替え）
- [ ] 設定画面（作業時間、休憩時間の変更）
- [ ] 通知音（セッション完了時）
- [ ] ブラウザ通知（Notification API）
- [ ] 履歴保存（Flask API と SQLite）
- [ ] グラフ表示（日別・週別の集中時間）
