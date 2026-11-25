import streamlit as st

st.set_page_config(page_title="헌혈 가능 여부 & 수혈 표", page_icon="🩸", layout="centered")

# 1. [리스트] 혈액형별 수혈 받을 수 있는 혈액형 데이터
transfusion_list = [
    ["A형", [["A형", "🟢 다량 수혈"], ["O형", "🟡 소량 수혈"]]],
    ["B형", [["B형", "🟢 다량 수혈"], ["O형", "🟡 소량 수혈"]]],
    ["O형", [["O형", "🟢 다량 수혈"]]],
    ["AB형", [["AB형", "🟢 다량 수혈"], ["A형", "🟡 소량 수혈"], ["B형", "🟡 소량 수혈"], ["O형", "🟡 소량 수혈"]]]
]

# 2. [함수] 성별, 나이, 몸무게를 입력받아 헌혈 가능 여부와 안내 메시지를 리턴
def check_donation(gender, age, weight):
    # [조건문] 만 16~69세, 남성 50kg 이상, 여성 45kg 이상 조건 확인
    if age < 16 or age > 69:
        return "연령제한", "🚨 헌혈 경고: 헌혈은 만 16세 이상 ~ 69세 이하만 가능합니다."
    elif gender == "남성" and weight < 50:
        return "체중제한", "🚨 헌혈 경고: 남성은 몸무게가 50kg 이상이어야 헌혈할 수 있습니다."
    elif gender == "여성" and weight < 45:
        return "체중제한", "🚨 헌혈 경고: 여성은 몸무게가 45kg 이상이어야 헌혈할 수 있습니다."
    else:
        return "가능", "💖 헌혈 권장: 모든 기준을 충족했습니다! 따뜻한 생명 나눔, 헌혈에 참여해 주세요!"

# --- 웹앱 화면 구성 ---
st.title("🩸 헌혈 자가진단 & 혈액형별 수혈 가이드")
st.write("성별, 나이, 몸무게와 혈액형을 입력하고 버튼을 눌러 결과를 확인하세요.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    gender = st.radio("성별을 선택하세요", ["남성", "여성"], horizontal=True)
    age = st.number_input("나이 (만 나이)", min_value=1, max_value=120, value=18, step=1)

with col2:
    weight = st.number_input("몸무게 (kg)", min_value=10.0, max_value=200.0, value=55.0, step=0.5)
    selected_blood = st.selectbox("본인의 혈액형을 선택하세요", ["A형", "B형", "O형", "AB형"])

if st.button("헌혈 가능 여부 및 수혈 표 확인하기 💉", use_container_width=True):
    st.divider()

    # 함수 호출
    status, message = check_donation(gender, age, weight)

    # 3. [조건문 - if-elif-else] 헌혈 가능 시 권장 메시지, 불가능 시 경고 문구 출력
    st.subheader("1️⃣ 헌혈 가능 여부 판정 결과")
    if status == "가능":
        st.success(message)
        st.balloons()
    elif status == "연령제한":
        st.error(message)
    else:
        st.warning(message)

    # 4. [반복문 - for] 리스트 데이터를 순회하며 '피 넘겨주는 귀여운 그림 표' 생성
    st.subheader(f"2️⃣ '{selected_blood}'이 수혈 받을 수 있는 혈액형 표")

    table_html = """
<table style="width:100%; border-collapse:collapse; text-align:center; border-radius:14px; overflow:hidden; box-shadow:0 3px 10px rgba(0,0,0,0.08);">
<thead>
<tr style="background-color:#ff6b6b; color:white; font-size:16px;">
<th style="padding:12px;">피 주는 혈액형</th>
<th style="padding:12px;">피 넘겨주는 귀여운 그림</th>
<th style="padding:12px;">피 받는 혈액형</th>
<th style="padding:12px;">수혈 구분</th>
</tr>
</thead>
<tbody>
"""

    for item in transfusion_list:
        if item[0] == selected_blood:
            donor_list = item[1]
            for donor_info in donor_list:
                donor = donor_info[0]
                t_type = donor_info[1]

                if "다량" in t_type:
                    arrow_color = "#2b8a3e"
                else:
                    arrow_color = "#f08c00"

                cute_svg = f"""
<svg width="170" height="54" viewBox="0 0 170 54" xmlns="http://www.w3.org/2000/svg">
  <path d="M28 8 C28 8 14 25 14 35 A14 14 0 0 0 42 35 C42 25 28 8 28 8 Z" fill="#ff4d4f"/>
  <circle cx="24" cy="33" r="1.8" fill="#ffffff"/>
  <circle cx="32" cy="33" r="1.8" fill="#ffffff"/>
  <path d="M25 38 Q28 41 31 38" stroke="#ffffff" stroke-width="1.8" fill="none" stroke-linecap="round"/>
  <line x1="50" y1="30" x2="112" y2="30" stroke="{arrow_color}" stroke-width="4" stroke-linecap="round"/>
  <polygon points="112,24 123,30 112,36" fill="{arrow_color}"/>
  <text x="78" y="21" font-size="14">💖</text>
  <circle cx="142" cy="31" r="15" fill="#ffd8a8" stroke="#ffa94d" stroke-width="2"/>
  <circle cx="137" cy="29" r="1.8" fill="#333333"/>
  <circle cx="147" cy="29" r="1.8" fill="#333333"/>
  <path d="M138 35 Q142 39 146 35" stroke="#e8590c" stroke-width="2" fill="none" stroke-linecap="round"/>
</svg>
"""

                table_html += f"""
<tr style="background-color:#fff5f5; border-bottom:1px solid #ffc9c9; font-size:15px;">
<td style="padding:10px; font-weight:bold; color:#c92a2a;">🩸 {donor}</td>
<td style="padding:8px;">{cute_svg}</td>
<td style="padding:10px; font-weight:bold; color:#1864ab;">🏥 {selected_blood}</td>
<td style="padding:10px; font-weight:bold;">{t_type}</td>
</tr>
"""

    table_html += """
</tbody>
</table>
"""
    st.markdown(table_html, unsafe_allow_html=True)
