# アーキテクチャ概要

## 現在の実装状態

### 全体構成

````text
1.pomodoro/
├── app.py                  # Flask アプリケーション（アプリファクトリ形式）
├── templates/
│   └── index.html          # メイン HTML テンプレート
└── static/
    ├── css/
    │   └── style.css       # スタイルシート
    └── js/
        └── app.js          # フロントエンドロジック（単一ファイル）
````

> **注意**: 当初のアーキテクチャ設計では JavaScript を複数モジュール（`timer-core.js`、`timer-ui.js`、`storage.js`、`app.js`）に分割する予定でしたが、現在の実装では `app.js` 単一ファイルに全ロジックがまとめられています。

---

## 各レイヤーの役割

### バックエンド（Flask）

- **`app.py`**: アプリファクトリ関数 `create_app()` を提供します。
  - `GET /` ルートを登録し、`index.html` テンプレートを返します。
  - 初期パラメータ（`work_minutes=25`、`break_minutes=5`）をテンプレートに渡します。
  - テスト用設定（`test_config`）を受け取れる柔軟な構造です。

### フロントエンド（HTML/CSS/JavaScript）

- **`templates/index.html`**: アプリケーションの HTML 構造を定義します。
  - サーバーから渡された設定を `window.POMODORO_CONFIG` に格納します。
- **`static/css/style.css`**: UI の見た目を定義します。
- **`static/js/app.js`**: タイマーのすべてのロジックと DOM 操作を担当します。

---

## データフロー

````text
ブラウザ
  │
  ├─ [起動時] GET / → Flask → render_template(index.html, work_minutes=25, break_minutes=5)
  │                  ↓
  │          index.html を配信（window.POMODORO_CONFIG に初期設定を埋め込み）
  │
  └─ [操作時] ユーザーがボタンをクリック
               ↓
          app.js がイベントを処理
               ↓
          状態（state オブジェクト）を更新
               ↓
          DOM を更新（残り時間、ステータス、プログレスリング等）
````

---

## 設計上の特徴

### アプリファクトリパターン

`create_app()` 関数でアプリケーションインスタンスを生成することで、通常起動とテスト起動を明確に分離しています。

````python
def create_app(test_config=None):
    app = Flask(__name__, ...)
    if test_config:
        app.config.update(test_config)
    # ルート登録
    return app
````

### クライアントサイドでの状態管理

タイマーの状態は JavaScript の `state` オブジェクトで管理されます。サーバーへの通信は発生しません（現時点では localStorage も未実装）。

### サーバー・クライアント間の設定受け渡し

Flask テンプレートの `{{ value | tojson }}` 記法を使って、サーバー側の設定値を JavaScript へ安全に渡します。

---

## 未実装の計画要素

当初の設計で予定されていたが、現時点では実装されていないものです。

| 要素 | 説明 |
|------|------|
| `timer-core.js` | タイマーロジックを DOM から分離した純粋関数モジュール |
| `timer-ui.js` | DOM 更新処理の専用モジュール |
| `storage.js` | localStorage による進捗の永続化モジュール |
| `tests/test_app.py` | Flask ルーティングのテスト |
| `tests/js/` | JavaScript ユニットテスト（Vitest） |
