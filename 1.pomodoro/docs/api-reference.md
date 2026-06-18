# API リファレンス

## 概要

現在の実装では、Flask は HTML 画面の配信のみを担当しています。REST API エンドポイントは未実装です。

---

## エンドポイント一覧

### `GET /`

メインページを返します。

#### リクエスト

````http
GET / HTTP/1.1
Host: localhost:5000
````

#### レスポンス

- **ステータスコード**: `200 OK`
- **Content-Type**: `text/html; charset=utf-8`
- **ボディ**: `templates/index.html` をレンダリングした HTML

#### テンプレート変数

Flask が `render_template` を呼び出す際に、以下の変数を HTML テンプレートに渡します。

| 変数名 | 型 | 値 | 説明 |
|--------|----|----|------|
| `work_minutes` | `int` | `25` | 作業セッションの時間（分） |
| `break_minutes` | `int` | `5` | 休憩セッションの時間（分） |

これらの値はテンプレート内の `<script>` ブロックで `window.POMODORO_CONFIG` オブジェクトに設定され、フロントエンド JavaScript から参照されます。

````html
<script>
    window.POMODORO_CONFIG = {
        workMinutes: {{ work_minutes | tojson }},
        breakMinutes: {{ break_minutes | tojson }},
    };
</script>
````

---

## 将来的な拡張予定（未実装）

将来的な機能拡張時に追加が想定されているエンドポイントです。現時点では実装されていません。

| メソッド | パス | 説明 |
|----------|------|------|
| `GET` | `/api/stats/today` | 今日の進捗（完了数、集中時間）を取得 |
| `POST` | `/api/sessions` | 完了したセッションを記録 |
