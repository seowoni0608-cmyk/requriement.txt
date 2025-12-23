import streamlit as st
import base64
import requests
import json
import time

# --- Configuration & Styling ---
st.set_page_config(page_title="나의 내면의 색깔 찾기", page_icon="✨", layout="centered")

# Custom CSS for Pastel Aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #fdf6f6;
    }
    
    .main {
        background-color: #fdf6f6;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        border: 1px solid #ffe4e1;
        background-color: white;
        color: #4a4a4a;
        padding: 15px;
        transition: all 0.3s ease;
        font-size: 16px;
    }
    
    .stButton>button:hover {
        border-color: #ffb6c1;
        background-color: #fffafa;
        color: #ff69b4;
        transform: translateY(-2px);
    }

    .result-card {
        background-color: white;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
    }

    .mbti-title {
        color: #ffb6c1;
        font-size: 42px;
        font-weight: 700;
        letter-spacing: 5px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Data Definition ---
questions = [
    {"q": "처음 보는 사람들과 함께 있는 파티에서 나는?", "options": [("먼저 말을 걸며 분위기를 주도한다", "E"), ("조용히 아는 사람 곁에 머문다", "I")]},
    {"q": "주말에 시간이 생겼을 때 나는?", "options": [("무조건 밖으로 나가서 사람들을 만난다", "E"), ("집에서 혼자만의 시간을 즐긴다", "I")]},
    {"q": "새로운 일을 시작할 때 나는?", "options": [("전체적인 흐름과 가능성을 본다", "N"), ("구체적인 정보와 실현 가능성을 본다", "S")]},
    {"q": "영화를 볼 때 나는?", "options": [("숨겨진 의미나 비유를 생각하며 본다", "N"), ("보여지는 상황과 액션에 집중한다", "S")]},
    {"q": "친구의 고민 상담을 해줄 때 나는?", "options": [("내 일처럼 공감하며 위로해준다", "F"), ("현실적인 해결책과 조언을 준다", "T")]},
    {"q": "선물을 고를 때 나는?", "options": [("상대방의 마음이 담긴 정성을 생각한다", "F"), ("상대방에게 정말 필요한 실용성을 생각한다", "T")]},
    {"q": "여행 계획을 세울 때 나는?", "options": [("시간별로 세부 일정을 꼼꼼하게 짠다", "J"), ("큰 틀만 잡고 상황에 맞게 움직인다", "P")]},
    {"q": "방 정리를 할 때 나는?", "options": [("항상 제자리에 정돈되어 있어야 마음이 편하다", "J"), ("어느 정도 어질러져 있어도 신경 쓰지 않는다", "P")]},
    {"q": "대화할 때 나는?", "options": [("생각나는 대로 즉흥적으로 말하는 편이다", "E"), ("머릿속으로 정리한 뒤 말하는 편이다", "I")]},
    {"q": "미래에 대해 생각할 때 나는?", "options": [("일어나지 않은 일들에 대한 상상을 즐긴다", "N"), ("현재 닥친 문제들을 해결하는 데 집중한다", "S")]},
    {"q": "비판을 들었을 때 나는?", "options": [("감정적으로 상처를 쉽게 받는다", "F"), ("객관적인 사실인지 따져본다", "T")]},
    {"q": "약속 시간이 정해지면 나는?", "options": [("늦지 않게 미리 준비해서 나가는 편이다", "J"), ("마지막 순간에 서둘러 나가는 편이다", "P")]}
]

mbti_desc = {
    'ENFP': '자유로운 영혼의 소유자. 매일이 새로운 모험인 당신!',
    'ENFJ': '정의로운 리더. 타인을 따뜻하게 감싸 안는 당신!',
    'ENTP': '뜨거운 논쟁을 즐기는 변론가. 창의적인 혁명가인 당신!',
    'ENTJ': '대담한 전략가. 목표를 향해 달려가는 당신!',
    'ESFP': '자유로운 영혼의 연예인. 삶을 파티처럼 즐기는 당신!',
    'ESFJ': '사교적인 외교관. 타인에게 헌신적인 당신!',
    'ESTP': '모험을 즐기는 사업가. 행동이 앞서는 당신!',
    'ESTJ': '엄격한 관리자. 체계적으로 리드하는 당신!',
    'INFP': '열정적인 중재자. 내면의 목소리에 귀 기울이는 당신!',
    'INFJ': '선의의 옹호자. 통찰력으로 세상을 바라보는 당신!',
    'INTP': '논리적인 사색가. 끊임없이 탐구하는 당신!',
    'INTJ': '용의주도한 전략가. 완벽함을 추구하는 당신!',
    'ISFP': '호기심 많은 예술가. 현재를 소중히 여기는 당신!',
    'ISFJ': '용감한 수호자. 묵묵히 자리를 지키는 당신!',
    'ISTP': '만능 재주꾼. 도구를 자유자재로 다루는 당신!',
    'ISTJ': '청렴결백한 논리주의자. 원칙을 중시하는 당신!'
}

# --- State Management ---
if 'step' not in st.session_state:
    st.session_state.step = 'start'
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# --- Functions ---
def generate_image(mbti):
    api_key = "" # API Key provided by environment
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={api_key}"
    prompt = f"A dreamy, minimal, high-quality pastel theme illustration for an {mbti} personality. Soft aesthetic, clean composition, artistic and calming. No text."
    
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1}
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        if 'predictions' in result:
            img_data = result['predictions'][0]['bytesBase64Encoded']
            return f"data:image/png;base64,{img_data}"
    except:
        return None
    return None

# --- UI Logic ---
if st.session_state.step == 'start':
    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-weight: 500;'>✨ 나의 내면의 색깔 찾기</h1>", unsafe_allow_html=True)
    st.write("12가지 질문을 통해 당신의 MBTI와 어울리는 테마를 알아보세요.")
    if st.button("테스트 시작하기"):
        st.session_state.step = 'quiz'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.step == 'quiz':
    idx = st.session_state.current_q
    progress = (idx + 1) / len(questions)
    
    st.progress(progress)
    st.write(f"질문 {idx + 1} / 12")
    st.markdown(f"### {questions[idx]['q']}")
    
    for option_text, val in questions[idx]['options']:
        if st.button(option_text, key=f"btn_{idx}_{val}"):
            st.session_state.answers.append(val)
            if st.session_state.current_q < len(questions) - 1:
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.session_state.step = 'result'
                st.rerun()

elif st.session_state.step == 'result':
    with st.spinner('당신의 색깔을 분석하는 중...'):
        time.sleep(1.5) # Simulating analysis
        
        # Calculate MBTI
        ans = st.session_state.answers
        # Logic to count types
        mbti = ""
        mbti += "E" if ans.count("E") >= ans.count("I") else "I"
        mbti += "N" if ans.count("N") >= ans.count("S") else "S"
        mbti += "F" if ans.count("F") >= ans.count("T") else "T"
        mbti += "P" if ans.count("P") >= ans.count("J") else "J"
        
        st.markdown(f"""
            <div class="result-card">
                <p style="color: #888;">당신에게 어울리는 색은</p>
                <h1 class="mbti-title">{mbti}</h1>
                <p style="font-size: 18px; color: #555;">{mbti_desc.get(mbti, "")}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Image Generation
        img_b64 = generate_image(mbti)
        if img_b64:
            st.markdown(f"<div style='margin-top: 20px; text-align: center;'><img src='{img_b64}' style='width: 100%; border-radius: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'></div>", unsafe_allow_html=True)
        else:
            st.info("테마 이미지를 생성하는 데 문제가 발생했습니다. (API 설정 확인 필요)")
            
        if st.button("다시 테스트하기"):
            st.session_state.step = 'start'
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.rerun()
