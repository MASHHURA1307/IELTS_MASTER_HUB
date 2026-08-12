from datetime import datetime

def raw_score_to_reading_band(raw_score, max_questions=40):
    """Convert Reading raw score (0-40) to IELTS Band (1.0-9.0)."""
    score = int(raw_score)
    if score >= 39: return 9.0
    if score >= 37: return 8.5
    if score >= 35: return 8.0
    if score >= 33: return 7.5
    if score >= 30: return 7.0
    if score >= 27: return 6.5
    if score >= 23: return 6.0
    if score >= 19: return 5.5
    if score >= 15: return 5.0
    if score >= 13: return 4.5
    if score >= 10: return 4.0
    if score >= 8:  return 3.5
    if score >= 6:  return 3.0
    if score >= 4:  return 2.5
    return 2.0 if score > 0 else 1.0

def raw_score_to_listening_band(raw_score, max_questions=40):
    """Convert Listening raw score (0-40) to IELTS Band (1.0-9.0)."""
    score = int(raw_score)
    if score >= 39: return 9.0
    if score >= 37: return 8.5
    if score >= 35: return 8.0
    if score >= 32: return 7.5
    if score >= 30: return 7.0
    if score >= 26: return 6.5
    if score >= 23: return 6.0
    if score >= 18: return 5.5
    if score >= 16: return 5.0
    if score >= 13: return 4.5
    if score >= 10: return 4.0
    if score >= 7:  return 3.5
    if score >= 5:  return 3.0
    return 2.5 if score > 0 else 1.0

def calculate_overall_band(listening, reading, writing, speaking):
    """Calculate IELTS Overall Band score, rounded to nearest half band."""
    scores = [float(listening), float(reading), float(writing), float(speaking)]
    avg = sum(scores) / 4.0
    fraction = avg - int(avg)
    if fraction < 0.25:
        return float(int(avg))
    elif fraction < 0.75:
        return float(int(avg)) + 0.5
    else:
        return float(int(avg)) + 1.0

def format_uzbek_date(dt):
    if not dt:
        return ""
    if isinstance(dt, str):
        return dt
    months_uz = [
        "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
        "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"
    ]
    return f"{dt.day}-{months_uz[dt.month - 1]}, {dt.year} {dt.strftime('%H:%M')}"

def get_user_badges(user_data, results_summary):
    """Generate dynamic achievement badges based on user performance."""
    badges = []
    
    # 1. Newbie
    badges.append({
        "id": "welcome",
        "name": "Boshlovchi",
        "desc": "IELTS Master Hub platformasiga a'zo bo'ldi",
        "icon": "bi-rocket-takeoff-fill",
        "color": "primary",
        "unlocked": True
    })
    
    # 2. Daily Streak
    streak = user_data.get("streak", 0)
    badges.append({
        "id": "streak_7",
        "name": "Intizomli Talaba",
        "desc": "7 kun uzluksiz tayyorgarlik ko'rdi",
        "icon": "bi-fire",
        "color": "warning",
        "unlocked": streak >= 7
    })
    
    # 3. High Reading Band
    reading_band = results_summary.get("reading_band", 0)
    badges.append({
        "id": "reading_master",
        "name": "Mutolaa Ustasi",
        "desc": "Reading bo'yicha 7.0 yoki undan yuqori natija",
        "icon": "bi-book-half",
        "color": "info",
        "unlocked": reading_band >= 7.0
    })

    # 4. Essay Master
    essay_count = results_summary.get("writing_count", 0)
    badges.append({
        "id": "writer",
        "name": "Insho Yozuvchi",
        "desc": "Kamida 5 ta Writing inshosini AI baholatdi",
        "icon": "bi-pencil-fill",
        "color": "success",
        "unlocked": essay_count >= 5
    })

    # 5. Mock Exam Completed
    mock_count = results_summary.get("mock_count", 0)
    badges.append({
        "id": "mock_warrior",
        "name": "Imtihon Qahramoni",
        "desc": "Kamida 1 ta to'liq Mock Exam topshirdi",
        "icon": "bi-award-fill",
        "color": "danger",
        "unlocked": mock_count >= 1
    })

    return badges
