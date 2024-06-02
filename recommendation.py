import pickle
import numpy as np
import pandas as pd
from scipy.spatial.distance import mahalanobis

# Mahalanobis 거리 계산 함수
def mahalanobis_distance(X, Y, inv_cov):
    diff = X - Y
    return np.sqrt(np.dot(np.dot(diff.T, inv_cov), diff))

# 최적의 데이터를 찾는 함수
def get_optimal_data(user_choice_diff, user_choice_place, user_choice_purpose, weights, colors):
    # 저장된 데이터 불러오기
    with open('data/clustering_data1.pkl', 'rb') as f:
        data = pickle.load(f)
    
    diff_pca = data['diff_pca']
    place_pca = data['place_pca']
    purpose_pca = data['purpose_pca']
    centroids_diff = data['centroids_diff']
    centroids_place = data['centroids_place']
    centroids_purpose = data['centroids_purpose']
    inv_cov_diff = data['inv_cov_diff']
    inv_cov_place = data['inv_cov_place']
    inv_cov_purpose = data['inv_cov_purpose']
    actual_grades_df = data['actual_grades_df']

    
    # 선택한 클러스터 중심점으로부터의 Mahalanobis 거리 계산
    distances_diff = np.array([mahalanobis_distance(row, centroids_diff[user_choice_diff], inv_cov_diff) for row in diff_pca])
    distances_place = np.array([mahalanobis_distance(row, centroids_place[user_choice_place], inv_cov_place) for row in place_pca])
    distances_purpose = np.array([mahalanobis_distance(row, centroids_purpose[user_choice_purpose], inv_cov_purpose) for row in purpose_pca])
    
    # 사용자가 선택한 클러스터에 대한 가중치 적용
    weighted_distances = distances_diff * weights[0] + distances_place * weights[1] + distances_purpose * weights[2]
    while True:
    # 가장 가까운 식물의 인덱스 찾기
        min_distance_idx = np.argmin(weighted_distances)
        dfdf = pd.DataFrame(actual_grades_df.iloc[min_distance_idx]).transpose()

        # '꽃 색깔' 열에서 특정 색상이 포함되어 있는지 확인
        try:
    # 사용자가 색상을 선택했는지 여부를 체크
            if colors:
                # 선택된 색상들 중 하나라도 '꽃 색깔' 필드에 포함되어 있는지 확인
                contains_any_color = any(color in dfdf['꽃 색깔'].iloc[0].split() for color in colors)
                if contains_any_color:
                    # 원하는 색상을 포함하는 식물을 찾았으면 반복을 종료
                    break
                else:
                    # 최소 거리로 선택된 식물의 인덱스를 무한대로 설정하여 다음 선택에서 제외
                    weighted_distances[min_distance_idx] = np.inf
            else:
                # 사용자가 아무 색상도 선택하지 않았다면 모든 식물을 대상으로 처리
                break
        except:
            # 예외 발생 시 현재 식물을 선택에서 제외
            weighted_distances[min_distance_idx] = np.inf
    # 매칭률 계산
    # np.inf 값을 제외하고 배열 필터링
    filtered_distances = weighted_distances[weighted_distances != np.inf]

    min_distance = weighted_distances[min_distance_idx]
    max_distance = filtered_distances.max()
    matching_rate = (1 - min_distance / max_distance) * 100  # 매칭률을 백분율로 변환
    
    return actual_grades_df.iloc[min_distance_idx], matching_rate
