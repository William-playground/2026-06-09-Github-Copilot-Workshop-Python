# ポモドーロタイマー Web アプリケーション アーキテクチャ案

## 目的

このドキュメントは、Flask、HTML、CSS、JavaScript を使用してポモドーロタイマー Web アプリケーションを実装するためのアーキテクチャ方針をまとめたものです。

添付 UI モックのような単一画面のタイマーアプリを、シンプルに実装しつつ、後から機能追加やユニットテストを行いやすい構成にすることを目的とします。

## 基本方針

このアプリケーションでは、Flask は画面配信と将来的な API の入口に限定し、タイマーの進行や画面更新はブラウザ側の JavaScript で管理します。

タイマーは 1 秒ごとに状態が変わる UI であるため、サーバー側で時間を管理するよりも、クライアント側で状態を持つ方が自然です。一方で、将来的に履歴保存やユーザー別の進捗管理を追加できるよう、Flask 側は拡張しやすい形にしておきます。

## ディレクトリ構成

```text
1.pomodoro/
  app.py
  templates/
    index.html
  static/
    css/
      style.css
    js/
      timer-core.js
      timer-ui.js
      storage.js
      app.js
    images/
      pomodoro.png
  tests/
    test_app.py
    js/
      timer-core.test.js
      storage.test.js
```

## 各ファイルの責務

| ファイル | 役割 |
| --- | --- |
| `app.py` | Flask アプリケーション本体。画面表示、初期値の受け渡し、将来的な API を担当します。 |
| `templates/index.html` | アプリ画面の HTML 構造を定義します。 |
| `static/css/style.css` | UI モックに沿った見た目を定義します。背景、カード、円形タイマー、ボタン、進捗表示を担当します。 |
| `static/js/timer-core.js` | タイマーの状態遷移ロジックを担当します。DOM や localStorage には依存させません。 |
| `static/js/timer-ui.js` | DOM 更新を担当します。残り時間、ステータス、円形プログレス、ボタン表示を画面に反映します。 |
| `static/js/storage.js` | 今日の進捗を localStorage に保存、復元します。日付変更時のリセットもここで扱います。 |
| `static/js/app.js` | 各モジュールを接続します。イベントリスナー登録、初期化、タイマー実行間隔の管理を担当します。 |
| `tests/test_app.py` | Flask のルーティングやテンプレート表示をテストします。 |
| `tests/js/*.test.js` | JavaScript のロジックをテストします。 |

## Flask 側の設計

Flask 側はアプリファクトリ形式にします。これにより、通常起動とテスト起動を分けやすくなります。

```python
from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)

    @app.route("/")
    def index():
        return render_template(
            "index.html",
            work_minutes=25,
            break_minutes=5,
        )

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
```

初期実装では、Flask の責務は `/` にアクセスしたときに画面を返すことです。

将来的に履歴保存を追加する場合は、次のような API を追加できます。

```text
GET  /api/stats/today
POST /api/sessions
```

ただし、初期実装ではデータベースを使わず、ブラウザの localStorage で進捗を保存します。

## フロントエンドの設計

### 画面構成

UI モックに合わせて、画面は次のような構造にします。

```text
body
  .app-shell
    .window
      .titlebar
      .status-label
      .timer-ring
      .actions
      .daily-summary
```

| UI 要素 | 内容 |
| --- | --- |
| タイトルバー | 「ポモドーロタイマー」と疑似ウィンドウ操作アイコンを表示します。 |
| ステータス | 「作業中」「休憩中」「停止中」など、現在の状態を表示します。 |
| 円形タイマー | 残り時間と進捗リングを表示します。 |
| 操作ボタン | 開始、一時停止、リセットを操作します。 |
| 今日の進捗 | 完了回数、集中時間を表示します。 |

### JavaScript の状態管理

タイマーの状態は 1 つのオブジェクトとして扱います。

```javascript
const state = {
  mode: "work",
  durationSeconds: 25 * 60,
  remainingSeconds: 25 * 60,
  isRunning: false,
  completedCount: 0,
  focusSeconds: 0,
  intervalId: null,
};
```

主な状態は次の通りです。

| プロパティ | 内容 |
| --- | --- |
| `mode` | 現在のモードです。初期実装では `work` を基本にします。将来的に `break` を追加できます。 |
| `durationSeconds` | 現在のセッション全体の秒数です。 |
| `remainingSeconds` | 残り秒数です。 |
| `isRunning` | タイマーが実行中かどうかを表します。 |
| `completedCount` | 今日完了したポモドーロ数です。 |
| `focusSeconds` | 今日の集中時間の合計秒数です。 |
| `intervalId` | `setInterval` の ID です。 |

## ユニットテストしやすい設計

テストしやすくするため、タイマーの状態遷移ロジックと DOM 操作を分離します。

最も重要なのは、`timer-core.js` を純粋関数中心にすることです。`timer-core.js` では `document.querySelector` や `localStorage` を直接使いません。入力された状態から新しい状態を返す関数を定義します。

```javascript
function tick(state) {
  if (!state.isRunning || state.remainingSeconds <= 0) {
    return state;
  }

  return {
    ...state,
    remainingSeconds: state.remainingSeconds - 1,
  };
}
```

このようにしておくと、ブラウザ画面を起動しなくても、状態遷移を単体テストできます。

```javascript
test("tick decreases remaining seconds while running", () => {
  const state = {
    isRunning: true,
    remainingSeconds: 1500,
  };

  expect(tick(state).remainingSeconds).toBe(1499);
});
```

### テスト対象の分け方

| 対象 | テスト内容 |
| --- | --- |
| `timer-core.js` | 開始、一時停止、リセット、1 秒経過、完了判定、表示用フォーマットをテストします。 |
| `storage.js` | localStorage への保存、復元、日付変更時のリセットをテストします。 |
| `timer-ui.js` | 必要に応じて jsdom を使い、DOM 更新をテストします。 |
| `app.js` | 詳細なロジックを持たせず、基本的には統合部分として扱います。 |
| `app.py` | Flask test client を使い、`/` が 200 を返すことや HTML が表示されることをテストします。 |

## 主要な JavaScript 関数

| 関数 | 役割 |
| --- | --- |
| `createInitialState()` | 初期状態を作成します。 |
| `startTimer(state)` | タイマーを実行中にします。 |
| `pauseTimer(state)` | タイマーを一時停止します。 |
| `resetTimer(state)` | 残り時間を初期値に戻します。 |
| `tick(state)` | 1 秒経過した状態を返します。 |
| `completeSession(state)` | セッション完了時に完了数と集中時間を更新します。 |
| `formatTime(seconds)` | 秒数を `25:00` のような表示形式に変換します。 |
| `getProgress(state)` | 円形プログレス表示用の進捗率を返します。 |

## データ保存方針

初期実装では、今日の進捗を localStorage に保存します。

```text
localStorage
  pomodoro.completedCount
  pomodoro.focusSeconds
  pomodoro.lastUpdatedDate
```

`pomodoro.lastUpdatedDate` に保存日を持たせ、日付が変わっていた場合は完了数と集中時間をリセットします。

将来的に複数日の履歴やユーザー別の保存が必要になった場合は、Flask に API を追加し、SQLite などのデータベースへ移行します。

## 推奨テストツール

| 領域 | ツール |
| --- | --- |
| Python | pytest |
| JavaScript | Vitest |
| DOM テスト | jsdom |

初期段階では、すべてを一度に整備する必要はありません。まずは Flask のルーティングテストと `timer-core.js` のユニットテストから始めるのが現実的です。

## 初期実装で確認するテスト観点

| 観点 | 内容 |
| --- | --- |
| Flask ルート | `/` が 200 を返すこと。 |
| 初期表示 | 25 分の作業タイマーとして初期化されること。 |
| タイマー開始 | `isRunning` が `true` になること。 |
| 一時停止 | `isRunning` が `false` になること。 |
| リセット | 残り時間が初期値に戻ること。 |
| 1 秒経過 | 実行中のときだけ `remainingSeconds` が減ること。 |
| 完了判定 | 残り時間が 0 になったとき、完了数と集中時間が更新されること。 |
| 時刻表示 | `1500` 秒が `25:00` と表示されること。 |
| 日付変更 | 前日の進捗が今日に持ち越されないこと。 |

## 実装順序

1. Flask のアプリファクトリと `/` ルートを作成します。
2. `templates/index.html` に UI の HTML 構造を作成します。
3. `static/css/style.css` で UI モックの見た目を再現します。
4. `static/js/timer-core.js` にタイマーの純粋ロジックを実装します。
5. `static/js/timer-ui.js` に DOM 更新処理を実装します。
6. `static/js/storage.js` に localStorage 保存処理を実装します。
7. `static/js/app.js` でイベント登録と各モジュールの接続を行います。
8. `tests/test_app.py` で Flask のルーティングテストを追加します。
9. `tests/js/timer-core.test.js` でタイマーの状態遷移テストを追加します。
10. 必要に応じて通知音、ブラウザ通知、休憩モード、履歴 API を追加します。

## 将来的な拡張案

| 機能 | 拡張方針 |
| --- | --- |
| 休憩モード | `mode` に `break` を追加し、作業完了後に休憩タイマーへ切り替えます。 |
| 長い休憩 | 4 回完了ごとに長い休憩へ切り替えるルールを追加します。 |
| 設定画面 | 作業時間、休憩時間、長い休憩時間を変更できるようにします。 |
| 通知音 | セッション完了時に音を鳴らします。 |
| ブラウザ通知 | Notification API を使って、タブが非アクティブでも完了を知らせます。 |
| 履歴保存 | Flask API と SQLite を使って日別の実績を保存します。 |
| グラフ表示 | 日別・週別の集中時間を可視化します。 |

## まとめ

このアプリケーションは、Flask を画面配信と将来の API の入口、JavaScript をタイマー本体、CSS を UI モック再現の担当として分離します。

さらに、JavaScript を `timer-core.js`、`timer-ui.js`、`storage.js`、`app.js` に分けることで、タイマーの状態遷移を DOM から独立させ、ユニットテストしやすい構成にします。

最初は DB なしの単一画面アプリとして完成させ、必要に応じて Flask API、SQLite、履歴表示へ拡張していく方針が適しています。
