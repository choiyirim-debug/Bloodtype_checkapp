# app.py
import streamlit as st
import Bloodtype_checkapp  # 위에서 만든 Bloodtype_checkapp.py 모듈 불러오기

st.set_page_config(page_title="Bloodtype Check App", page_icon="🩸", layout="centered")

st.title("🩸 헌혈 가능 여부 & 혈액형별 수혈 표")
st.write("성별, 나이, 몸무게와 혈액형을 입력한 뒤 아래 버튼을 눌러주세요.")

st.divider()

# 사용자 입력 UI
col1, col2 = st.columns(2)
with col1:
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    age = st.number_input("나이 (만 나이)", min_value=1, max_value=120, value=18, step=1)

with col2:
    weight = st.number_input("몸무게 (kg)", min_value=10.0, max_value=200.0, value=55.0, step=0.5)
    blood_type = st.selectbox("혈액형 선택", ["A형", "B형", "O형", "AB형"])

# 확인 버튼
if st.button("결과 확인하기 💉", use_container_width=True):
    st.divider()

    # Bloodtype_checkapp 라이브러리의 함수 호출
    is_possible, result_message = Bloodtype_checkapp.check_donation(gender, age, weight)

    # [조건문] 헌혈 가능 시 권장 메시지, 불가능 시 경고 문구 출력
    st.subheader("1️⃣ 헌혈 가능 여부 판정")
    if is_possible == True:
        st.success(result_message)
        st.balloons()
    elif gender == "남성" and weight < 50:
        st.error(result_message)
    elif gender == "여성" and weight < 45:
        st.error(result_message)
    else:
        st.warning(result_message)

    # [반복문] 리스트에서 선택한 혈액형 데이터를 찾아 '피 넘겨주는 귀여운 그림 표' 생성
    st.subheader(f"2️⃣ {blood_type}이 수혈 받을 수 있는 혈액형 표")

    table_html = """
<table style="width:100%; border-collapse:collapse; text-align:center; border-radius:12px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
<thead>
<tr style="background-color:#ff6b6b; color:white; font-size:16px;">
<th style="padding:12px;">피 주는 혈액형</th>
<th style="padding:12px;">피 넘겨주는 그림</th>
<th style="padding:12px;">피 받는 혈액형</th>
<th style="padding:12px;">수혈 구분</th>
</tr>
</thead>
<tbody>
"""

    for data in Bloodtype_checkapp.blood_transfusion_list:
        if data[0] == blood_type:
            compatible_list = data[1]  # [[주는 혈액형, 수혈 종류], ...]
            for donor_info in compatible_list:
                donor_blood = donor_info[0]
                transfusion_type = donor_info[1]

                # 다량/소량 수혈에 따라 화살표 색상 다르게 표시
                if "다량" in transfusion_type:
                    arrow_style = "color:#2b8a3e; font-weight:bold;"
                else:
                    arrow_style = "color:#e67700; font-weight:bold;"

                table_html += f"""
<tr style="background-color:#fff5f5; border-bottom:1px solid #ffc9c9; font-size:15px;">
<td style="padding:14px; font-weight:bold; color:#c92a2a;">🩸 {donor_blood}</td>
<td style="padding:14px; font-size:20px;">
<span>😊🩸</span>
<span style="{arrow_style}"> ➔💉➔ </span>
<span>💖🥰</span>
</td>
<td style="padding:14px; font-weight:bold; color:#1864ab;">🏥 {blood_type}</td>
<td style="padding:14px; font-weight:bold;">{transfusion_type}</td>
</tr>
"""

    table_html += """
</tbody>
</table>
"""
    st.markdown(table_html, unsafe_allow_html=True)
