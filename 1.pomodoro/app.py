"""
ポモドーロタイマー Flask アプリケーション

Flask アプリファクトリ形式で実装。
通常起動とテスト起動を分けやすくするための設計。
"""

import os

from flask import Flask, render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app(test_config=None):
    """
    Flask アプリケーションを生成するファクトリ関数。
    
    Args:
        test_config: テスト用の設定（辞書）
    
    Returns:
        Flask アプリケーションインスタンス
    """
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
    )

    if test_config:
        app.config.update(test_config)

    @app.route("/")
    def index():
        """メインページを表示"""
        return render_template(
            "index.html",
            work_minutes=25,
            break_minutes=5,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
