import streamlit as st
import pandas as pd
import json
import os
import time
from datetime import datetime, timedelta

STATS_FILE = "stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {
        "xp": 0,
        "level": 1,
        "completed_pomodoros": 0,
        "streak_days": 0,
        "last_active_date": None,
        "badges": [],
        "history": []
    }

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

def check_badges(stats):
    new_badges = []
    
    if stats["streak_days"] >= 3 and "3日連続" not in stats["badges"]:
        stats["badges"].append("3日連続")
        new_badges.append("3日連続")
        
    if stats["streak_days"] >= 7 and "7日連続" not in stats["badges"]:
        stats["badges"].append("7日連続")
        new_badges.append("7日連続")
        
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    
    this_week_completions = sum(
        1 for h in stats["history"]
        if datetime.strptime(h["date"], "%Y-%m-%d") >= start_of_week
    )
    
    if this_week_completions >= 10 and "今週10回完了" not in stats["badges"]:
        stats["badges"].append("今週10回完了")
        new_badges.append("今週10回完了")
        
    return new_badges

def complete_pomodoro(stats):
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check streak
    last_active = stats["last_active_date"]
    if last_active:
        last_date = datetime.strptime(last_active, "%Y-%m-%d")
        current_date = datetime.strptime(today, "%Y-%m-%d")
        diff = (current_date - last_date).days
        
        if diff == 1:
            stats["streak_days"] += 1
        elif diff > 1:
            stats["streak_days"] = 1
    else:
        stats["streak_days"] = 1
        
    stats["last_active_date"] = today
    stats["completed_pomodoros"] += 1
    stats["xp"] += 50
    
    # Level up logic
    next_level_xp = stats["level"] * 100
    if stats["xp"] >= next_level_xp:
        stats["xp"] -= next_level_xp
        stats["level"] += 1
        st.balloons()
        st.success(f"🎉 レベルアップ！ レベル {stats['level']} になりました！")
        
    stats["history"].append({
        "date": today,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "focus_time": 25 # in minutes
    })
    
    new_badges = check_badges(stats)
    for badge in new_badges:
        st.success(f"🏆 新しいバッジを獲得しました: {badge}")
        
    save_stats(stats)
    return stats

st.set_page_config(page_title="Gamified Pomodoro", page_icon="🍅", layout="wide")

st.title("🍅 ゲーミフィケーション ポモドーロタイマー")

# Initialize session state
if 'stats' not in st.session_state:
    st.session_state.stats = load_stats()

stats = st.session_state.stats

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🌟 レベル", stats["level"])
with col2:
    st.metric("✨ XP", f"{stats['xp']} / {stats['level']*100}")
with col3:
    st.metric("🔥 ストリーク", f"{stats['streak_days']} 日")
with col4:
    st.metric("✅ 完了数", stats["completed_pomodoros"])

st.progress(stats["xp"] / (stats["level"] * 100))

# Timer Section
st.header("⏱️ タイマー")

if st.button("25分のポモドーロを完了する (デモ用)"):
    stats = complete_pomodoro(stats)
    st.session_state.stats = stats
    st.success("ポモドーロを完了しました！ +50 XP")

st.divider()

# Badges Section
st.header("🏆 獲得したバッジ")
if not stats["badges"]:
    st.info("まだバッジを獲得していません。ポモドーロを続けてバッジを集めましょう！")
else:
    cols = st.columns(len(stats["badges"]) if len(stats["badges"]) < 6 else 6)
    for i, badge in enumerate(stats["badges"]):
        with cols[i % 6]:
            st.button(badge, key=f"badge_{i}", disabled=True)

st.divider()

# Statistics Section
st.header("📊 統計グラフ")
if not stats["history"]:
    st.info("データがありません。")
else:
    # Convert history to DataFrame
    df = pd.DataFrame(stats["history"])
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate some metrics
    total_focus_time = df['focus_time'].sum()
    avg_focus_time = df['focus_time'].mean()
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("⏳ 合計集中時間", f"{total_focus_time} 分")
    with col_stat2:
        st.metric("📊 1回あたりの平均集中時間", f"{avg_focus_time:.1f} 分")
        
    st.subheader("直近の活動 (完了数)")
    daily_completions = df.groupby(df['date'].dt.date).size().reset_index(name='completions')
    daily_completions = daily_completions.set_index('date')
    
    st.bar_chart(daily_completions['completions'])
