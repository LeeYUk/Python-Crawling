import pandas as pd
import time
from tqdm.auto import tqdm
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#출처 https://hyunhp.tistory.com/12
#크롤링 전 세팅
chrome_driver_path = r'(C:/Users/이용욱/Desktop/python)' #크롬드라이브 설치 경로

url_path = 'https://youtu.be/3H7ojyexJlg' #크롤링 URL 나중에 찾고 싶은 영상 URL만 변경

#크롤링 반복 횟수
repeat = 3

# 댓글 작성자
commenter_let = []

#댓글
comment_let = []

#좋아요 개수
like_count_let = []

#하트 여부
heart_exist_let =[]

with Chrome(executable_path = chrome_driver_path) as driver:
    #찾으려는 대상이 불러올 때까지 지정된 시간만큼 대기하도록 설정한다.
    #인자는 초(second) 단위이며 ,  Default 값은 0초이다.
    wait = WebDriverWait(driver, 20)
    driver.get(url_path) # 영상url
    time.sleep(3)

#유튜브 실행 시 자동 영상 재생일 경우 , 영상 종료되면 바로 다음 영상으로 넘어가게 된다.
#이를 방지하기 위해 , 유튜브 영상 중지 후 크롤링 진행
if driver.find_element("ytp-play-button").get_attribute('aria-label')=='일시중지(k)': #출처에서는 driver.find_element_by_class_name 이 였으나  현재는 driver.find_element까지 씀
    driver.find_element("ytp-play-button").click()
else:
    pass

#최초 1회 PAGE_DOWN
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
time.sleep(3)

#END 반복 실행
#실행 횟수 체크
for item in tqdm(range(repeat)): #END버튼 반복 횟수 , 1회당 20개씩 댓글 업데이트
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
    time.sleep(3) #END버튼 클릭 이후, 1초 대기 후, 다시 END 버튼 진행

#크롤링 데이터 수집 진행

#작성자 가져오기
#댓글 작성자 중 확인된 사용자, 공식 아티스트 채널 값은 text로 가져올 시, (공백) 처리됨
try:
    for commenter in tqdm(wait.until(EC.presence_of_all_element_located((By.CSS_SELECTOR, '#author-text')))):
        #작성자 이름 없는 경우에, 공백 표시
        #확인된 사용자, 공식 아티스트 채넉의 경우, innertext를 가져옴
        if commenter.text !='':
            commenter_let.append(commenter.text)
        else:
            commenter_temp=commenter.get_attribute("innerText").strip().replace('\n','')
            commenter_let.append(commenter_temp)
except:
    #크롤링 값이 없을 경우
    commenter_let.append('')

#댓글 가져오기
try:
    for comment in tqdm(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#content-text')))):
        if comment.text !='':
            comment_temp=comment.text.replace('\n','')
            comment_let.append(comment_temp)
        else:
            comment_let.append('')
except:
    #크롤링 값이 없을 경우에
    comment_let.append('')

#좋아요 갯수 가져오기
try:
    for like_count in tqdm(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#vote-count-middle')))):
        if like_count.text !='':
            like_count_let.append(like_count.text)
        else:
            like_count_let.append('0')
except:
    # 좋아요 갯수가 없을 경우
    like_count_let.append('0')

#크리에이터 하트 여부 체크
for creater_heart in tqdm(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'creator-heart')))):
    #크리에이터 하트html 존재 여부로 체크
    try:
        if creater_heart.find_element_by_css_selector('#creator-heart-button'):
            heart_exist_let.append('하트')
        else:
            heart_exist_let.append('없음')
    except:
        #크롤링 값이 없을 경우
        heart_exist_let.append('없음')
        
print('done')

#저장위치
save_path=r'(C:/Users/이용욱/Desktop/임시폴더)'
df =pd.DataFrame({'댓글 작성자' : commenter_let,
                  '댓글'  :comment_let,
                  '좋아요 갯수' :like_count_let,
                  '하트 유/무' :heart_exist_let})
#index 1부터 실행
df.index=df.index+1

#to_csv 저장
df.to_csv(save_path + '유튜브 댓글 크롤링' + str((repeat +1)*20)+'개 크롤링.csv', encoding='utf-8-sig')

print('save done')

#출처 https://hyunhp.tistory.com/12