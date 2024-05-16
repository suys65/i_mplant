from sklearn.ensemble import RandomForestRegressor
import numpy as np

def calculate_Gn(A_nk):
    n = len(A_nk)
    Gn = round(sum(A_nk) / n)
    return Gn

def calculate_A(G_values, R_values):
    n = len(G_values)
    matches = [1 - abs(G - R) for G, R in zip(G_values, R_values)]
    A_percentage = (sum(matches) / n) * 100
    return A_percentage

def calculate_weights(I_nk):
    k = len(I_nk[0])
    weights = [round(sum(In) / k, 2) for In in I_nk]
    return weights

def calculate_C(G, M):
    m = 5  # Assuming 1 to 5 scale
    match = 1 - abs(G - M) / (m - 1)
    C_percentage = match * 100
    return C_percentage

def calculate_final_matching(Cn, Wn):
    final_match = sum(C * W for C, W in zip(Cn, Wn))
    return final_match

def calculate_final_matching_rate(A, R):
    Pn = (A + R) / 2
    return Pn

def matching_system(A_nk, R_values, I_nk, M_values):
    # Step 1: Calculate G_n
    G_values = [calculate_Gn(A) for A in A_nk]
    
    # Step 2: Calculate A(%)
    A_percentage = calculate_A(G_values, R_values)
    
    # Step 3: Calculate weights
    weights = calculate_weights(I_nk)
    
    # Step 4: Calculate C (Matching rate for each feature)
    C_values = [calculate_C(G, M) for G, M in zip(G_values, M_values)]
    
    # Step 5: Calculate final matching using weights and C values
    final_match = calculate_final_matching(C_values, weights)
    
    # Step 6: Calculate final matching rate P_n
    final_matching_rate = calculate_final_matching_rate(A_percentage, final_match)
    
    return final_matching_rate

def recommend_best_product(products, R_values, I_nk):
    best_match = 0
    best_product = None
    
    for product in products:
        A_nk = product['A_nk']
        M_values = product['M_values']
        match_rate = matching_system(A_nk, R_values, I_nk, M_values)
        
        if match_rate > best_match:
            best_match = match_rate
            best_product = product
    
    return best_product, best_match

# 예제 데이터 (혜림이의 정보를 바탕으로 예제 데이터를 제공합니다.)
products = [
    {
        'name': 'Product 1',
        'A_nk': [
            [4, 3, 4],  # Example data for A_nk
            [3, 4, 5],
        ],
        'M_values': [3, 3, 2]  # Example M values
    },
    {
        'name': 'Product 2',
        'A_nk': [
            [2, 3, 5],  # Example data for A_nk
            [3, 2, 4],
        ],
        'M_values': [2, 3, 5]  # Example M values
    },
    # Add more products here
]

R_values = [3, 4, 2]  # Example R values
I_nk = [
    [0.36, 0.42, 0.30],  # Example weight calculations
    [0.4, 0.5, 0.3],
]
# 가장 매칭률이 높은 상품 추천
best_product, best_match = recommend_best_product(products, R_values, I_nk)
print(f"추천 상품: {best_product['name']}, 매칭률: {best_match:.2f}%")
#---------------------------------------------------------------------------------------------------------------------#

# 특징 중요도 학습을 위한 데이터 준비
X = []
y = []

for product in products:
    for A in product['A_nk']:
        for I, M in zip(I_nk, product['M_values']):
            X.append(A + I)  # A와 I를 합쳐서 특징 벡터 생성
            y.append(M)      # 각 M 값을 y에 추가

X = np.array(X)
y = np.array(y)

# 랜덤 포레스트 회귀 모델 학습
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 특징 중요도 출력
importances = model.feature_importances_
print("Feature importances:", importances)

# 중요도를 기반으로 가중치 재계산
def calculate_weights_with_importance(I_nk, importances):
    weights = [round(sum(In * importances[:len(In)]) / len(In), 2) for In in I_nk]
    return weights

weights = calculate_weights_with_importance(I_nk, importances)
print("Updated weights:", weights)

# 기존 매칭 시스템 함수와 통합
def matching_system_with_importance(A_nk, R_values, I_nk, M_values, importances):
    G_values = [calculate_Gn(A) for A in A_nk]
    A_percentage = calculate_A(G_values, R_values)
    weights = calculate_weights_with_importance(I_nk, importances)
    C_values = [calculate_C(G, M) for G, M in zip(G_values, M_values)]
    final_match = calculate_final_matching(C_values, weights)
    final_matching_rate = calculate_final_matching_rate(A_percentage, final_match)
    return final_matching_rate

# 가장 매칭률이 높은 상품 추천
best_match = 0
best_product = None

for product in products:
    A_nk = product['A_nk']
    M_values = product['M_values']
    match_rate = matching_system_with_importance(A_nk, R_values, I_nk, M_values, importances)
    
    if match_rate > best_match:
        best_match = match_rate
        best_product = product

print(f"머신러닝 추천 상품: {best_product['name']}, 매칭률: {best_match:.2f}%")