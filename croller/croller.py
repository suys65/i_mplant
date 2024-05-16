from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.common.exceptions import TimeoutException
# ChromeDriver의 경로를 지정합니다. 여러분의 환경에 맞도록 수정하세요.
webdriver_path = 'c:/my_code/croller/chromedriver.exe'

# Selenium WebDriver 초기화
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service)

# 웹페이지 로드
driver.get('https://www.picturethisai.com/ko/wiki/Epipremnum_aureum.html')
driver.maximize_window()
wait = WebDriverWait(driver, 10)
# 검색창을 여는 버튼을 클릭하기 위한 요소를 찾습니다. CSS 선택자를 사용합니다.
search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#top_content > div > div.header-wrap-top-main-content-search-wrap > div")))
search_button.click()

# 검색창에 "000"을 입력합니다. 검색창의 요소를 찾기 위한 적절한 선택자를 사용해야 합니다.
# 여기서는 예시를 위해 검색창의 CSS 선택자가 '#search_input'라고 가정합니다.
search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#search")))
search_input.send_keys("튤립")

# Enter 키를 눌러 검색을 실행합니다.
search_input.send_keys(Keys.ENTER)
keys = [
            "수명", "종류", "재배 시기", "개화 시기", "수확 시기",
            "식물 높이", "꼭대기 지름", "잎 색깔", "꽃 지름", "꽃 색깔",
            "과일 색", "줄기 색상", "휴면", "잎 종류", "이상적인 온도", "성장기",
            "Pollinators", "Benefits to Pollinating Insects", "성장률"]

def create_dict_from_list(data, keys):
            result_dict = {}
            current_key = None
            for item in data:
                if item in keys:
                    # 현재 item이 keys에 있다면, 새로운 키로 설정
                    current_key = item
                    result_dict[current_key] = []
                elif current_key:
                    # 현재 키가 설정되어 있고, item이 keys에 없다면 현재 키의 값으로 추가
                    result_dict[current_key].append(item)
            
            # 리스트 내 단일 요소를 가진 키의 값들을 단일 값으로 변환
            for key in result_dict:
                if len(result_dict[key]) == 1:
                    result_dict[key] = result_dict[key][0]
                # 문자열에 쉼표가 있는 경우, 리스트로 분리
                elif len(result_dict[key]) == 1 and ',' in result_dict[key][0]:
                    result_dict[key] = [x.strip() for x in result_dict[key][0].split(',')]
            
            return result_dict
#------------------------------------------------------------------------------------------------------------------------------------#
index = 1  # 시작 인덱스
all_plant={}

while True:
    try:
        # CSS 선택자에서 인덱스 부분을 변수로 대체
        css_selector = f"#pcsearchContent > div:nth-child({index}) > img"
        # 지정한 CSS 선택자를 사용해 요소가 클릭 가능할 때까지 기다림
        image_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        image_element.click()
        #---------------------------------------------------------------------------------------#


        # 요소가 로드될 때까지 대기
        element_selector = "#plant_info_layout > div > div.plant-info-wrap > div > div:nth-child(1)"

        # 요소가 로드될 때까지 기다립니다.
        try:
            element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
            )
        except:
            driver.back()
            index += 1
            continue
        data = element.text.split('\n')  # 요소의 텍스트를 줄바꿈으로 나누어 리스트로 변환
        #print(data)

        # 데이터를 딕셔너리로 변환
        result_dict = {data[0]: create_dict_from_list(data[1:], keys)}

        #print(result_dict)
        all_plant.update(result_dict)
        index += 1
        driver.back()
    except TimeoutException:
        break

# 드라이버 종료
driver.quit()
#print(all_plant)
df = pd.DataFrame.from_dict(all_plant, orient='index')
columns_order = keys
df = df.reindex(columns=columns_order)
# 인덱스에서 "의 특성" 제거
df.index = df.index.str.replace('의 특성', '')
df
