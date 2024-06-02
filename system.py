# app.py
import streamlit as st
import pandas as pd
from recommendation import get_optimal_data
import streamlit as st
import pickle

product = pd.read_csv('data/product.csv', encoding='utf-8')

# 애플리케이션 제목
st.title('식물 추천 시스템')

# 마크다운을 사용하여 커스텀 라벨 생성
st.markdown("##### **1. 난이도를 선택하세요**")

# 라벨을 공백으로 두고 selectbox 생성
difficulty = st.selectbox('*무관 가능', ['순둥이', '든든이', '까칠이', "무관"])
# 선택한 난이도에 따라 user_difficulty 설정
if difficulty == '순둥이':
    user_difficulty = 3
elif difficulty == '든든이':
    user_difficulty = 2
elif difficulty == '까칠이':
    user_difficulty = 6
elif difficulty == '무관':
    user_difficulty = 6 

difficulty_weight = st.slider('난이도 중요도', min_value=0.1, max_value=10.0, value=5.0)

if difficulty == "무관" :
    difficulty_weight = 0

# 마크다운을 사용하여 커스텀 라벨 생성
st.markdown("##### **2. 장소를 선택하세요**")
place = st.selectbox('*무관 가능', ['거실','서재','베란다','가게','실외', "무관"])
if place == '거실':
    user_place = 1
elif place == '서재':
    user_place = 3
elif place == '베란다':
    user_place = 4
elif place == '가게':
    user_place = 0
elif place == '실외':
    user_place = 2
elif place == '무관':
    user_place = 2

place_weight = st.slider('장소 중요도', min_value=0.1, max_value=10.0, value=5.0)

if place == "무관" :
    place_weight = 0

st.markdown("##### **3. 용도를 선택하세요**")
purpose = st.selectbox('*무관 가능', ['인테리어 용','공기정화 용','선물 용','취미 용', "무관"])
# 선택한 용도에 따라 user_purpose 설정
if purpose == '인테리어 용':
    user_purpose = 2
elif purpose == '공기정화 용':
    user_purpose = 4
elif purpose == '선물 용':
    user_purpose = 1
elif purpose == '취미 용':
    user_purpose = 5
elif purpose == '무관':
    user_purpose = 5

purpose_weight = st.slider('용도 중요도', min_value=0.1, max_value=10.0, value=5.0)
if purpose == "무관" :
    purpose_weight = 0

st.markdown("##### **4. 꽃 색상을 선택하세요**")
#color = st.selectbox('꽃 색상을 선택하세요', ['흰색', '빨간색', '노란색', '파란색', '분홍색','초록색','보라색'])
colors = st.multiselect(
    '*복수선택 가능',
    ['흰색', '빨간색', '노란색', '파란색', '분홍색', '초록색', '보라색']
)

weights = [difficulty_weight, place_weight, purpose_weight]

# 추천 결과 가져오기
if st.button('추천받기'):
    recommendations, matching_rate = get_optimal_data(user_difficulty, user_place, user_purpose, weights, colors)

    if isinstance(recommendations, str):
        st.write(recommendations)
    else:
        st.markdown(f"#### **추천된 식물 : {recommendations.name}**")
        st.write(f"매칭률: {matching_rate:.2f}%")
        st.dataframe(recommendations[['수명','개화 시기','최대식물높이','꽃 색깔','최대 이상적 온도(℃)','water','sunlight']], width=1000)
#'종류', '수명', '개화 시기','점수용 최대식물높이','점수용 잎 종류','꽃 색깔','이상적인 온도','water','sunlight'
#임시
        #recommendation = '단풍나무'
        # 상품 정보 찾기
        result = product[product['식물 이름 1'] == recommendations.name]    #recommendations.name

        if not result.empty:
            st.markdown("### **온플에는 이런 상품이 있어요!**")
            for index, row in result.iterrows():
                col1, col2 = st.columns([1, 2])  # 페이지를 1:2 비율로 두 열로 나눔

                # 첫 번째 열(왼쪽)에는 상품 이미지를 배치
                with col1:
                # 상품 이미지
                    st.image(row['큰이미지'], caption=row['기존 상품명'], use_column_width=True)
                with col2:
                # 상품명과 입점업체ID (볼드체 및 크기 조정)
                    st.markdown(f"#### **{row['기존 상품명']}**")
                    st.text(f"{row['식물이름(학명) 1']}")
                    
                    # 상품판매가 (강조)
                    st.metric(label="상품판매가", value=f"{row['상품판매가']}원")
                    
                    # 대 카테고리와 중 카테고리
                    st.text(f"카테고리: {row['대 카테고리']} -> {row['중 카테고리']}")

                    # 상품 상세 페이지로 이동하는 링크 생성
                    product_url = f"https://www.on-ple.com/product/content.asp?guid={row['상품번호']}"
                    st.markdown(f"[온플로 해당상품 보러가기]({product_url})", unsafe_allow_html=True)

        else:
            st.error("해당 상품을 찾을 수 없습니다.")

# 버튼을 초록색으로 꾸미기 위한 CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: green;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

