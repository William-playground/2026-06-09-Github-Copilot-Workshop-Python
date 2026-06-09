/**
 * ポモドーロタイマー - メインアプリケーション
 * 
 * 各モジュールを接続し、イベントリスナーを登録します。
 * フェーズ 1 では基本的な初期化のみを行います。
 */

// DOM 要素の取得
const timerText = document.getElementById('timer-text');
const statusText = document.getElementById('status-text');
const startBtn = document.getElementById('start-btn');
const resetBtn = document.getElementById('reset-btn');
const completedCount = document.getElementById('completed-count');
const focusHours = document.getElementById('focus-hours');
const progressRing = document.getElementById('progress-ring');

// アプリケーション状態の初期化
const state = {
    mode: 'work',
    durationSeconds: 25 * 60,
    remainingSeconds: 25 * 60,
    isRunning: false,
    completedCount: 0,
    focusSeconds: 0,
    intervalId: null,
};

/**
 * 秒数を "MM:SS" 形式にフォーマット
 * @param {number} seconds - 秒数
 * @returns {string} フォーマットされた時間文字列
 */
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

/**
 * UI を更新
 */
function updateUI() {
    // 残り時間の更新
    timerText.textContent = formatTime(state.remainingSeconds);

    // ステータスの更新
    if (state.isRunning) {
        statusText.textContent = '作業中';
    } else {
        statusText.textContent = '停止中';
    }

    // ボタンテキストの更新
    if (state.isRunning) {
        startBtn.textContent = '一時停止';
    } else {
        startBtn.textContent = '開始';
    }

    // 進捗表示の更新
    completedCount.textContent = state.completedCount;
    
    const hours = Math.floor(state.focusSeconds / 3600);
    const minutes = Math.floor((state.focusSeconds % 3600) / 60);
    focusHours.textContent = `${hours}時間${minutes}分`;

    // 円形プログレスの更新
    const progress = (state.durationSeconds - state.remainingSeconds) / state.durationSeconds;
    const circumference = 2 * Math.PI * 90; // r = 90
    const offset = circumference * (1 - progress);
    progressRing.style.strokeDashoffset = offset;
}

/**
 * タイマー開始
 */
function startTimer() {
    if (state.isRunning) {
        // 一時停止
        state.isRunning = false;
        if (state.intervalId !== null) {
            clearInterval(state.intervalId);
            state.intervalId = null;
        }
    } else {
        // 開始
        state.isRunning = true;
        state.intervalId = setInterval(() => {
            if (state.remainingSeconds > 0) {
                state.remainingSeconds -= 1;
                updateUI();
            } else {
                // セッション完了
                state.completedCount += 1;
                state.focusSeconds += state.durationSeconds;
                state.remainingSeconds = state.durationSeconds;
                state.isRunning = false;
                clearInterval(state.intervalId);
                state.intervalId = null;
                updateUI();
                alert('セッション完了！休憩しましょう。');
            }
        }, 1000);
    }
    updateUI();
}

/**
 * タイマーリセット
 */
function resetTimer() {
    state.isRunning = false;
    state.remainingSeconds = state.durationSeconds;
    if (state.intervalId !== null) {
        clearInterval(state.intervalId);
        state.intervalId = null;
    }
    updateUI();
}

/**
 * イベントリスナーの登録
 */
startBtn.addEventListener('click', startTimer);
resetBtn.addEventListener('click', resetTimer);

/**
 * 初期表示
 */
updateUI();
