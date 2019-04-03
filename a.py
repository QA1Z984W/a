from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys

import sys
import time

# 강의실 입장 전
courseIndex = 1
courseRow = 1

# 강의 영상 인덱스
courseContentsIndex = 1
courseContentsRow = 2
courseContentsColumn = 1

driver = webdriver.Chrome(executable_path = 'chromedriver.exe')
driver.get('https://portal.dju.ac.kr')

# 포털 로그인
print("학번 입력 : ", end="")
hakbeon = input()

print("암호 입력 : ", end="")
password = input()

driver.find_element_by_name('login').send_keys(hakbeon)
driver.find_element_by_name('p').send_keys(password)
driver.find_element_by_id('loginImg').click()

time.sleep(2)

# 포털 => 사이버교육시스템
driver.get('https://lms.dju.ac.kr/sso/sso.jsp')

# 사이버교육시스템 => 진행중강의
driver.get('https://lms.dju.ac.kr/lms/myLecture/doListView.dunet')

print("==================== 연도 선택 ====================")
print("2019년 : [ 2019 ]\n2018년 : [ 2018 ]\n2017년 : [ 2017 ]\n2016년 : [ 2016 ]\n2015년 : [ 2015 ]\n2014년 : [ 2014 ]\n")
print("연도 입력 : ", end="")
year = input()
print()

selectYear = Select(driver.find_element_by_id('term_year'))
selectYear.select_by_value(year)

print("==================== 학기 선택 ====================")
print("1학기        : [ 1학기 ]\n2학기        : [ 2학기 ]\n여름학기     : [ 여름 계절학기 ]\n겨울학기     : [ 겨울 계절학기 ]\n")
print("학기 입력 : ", end="")
semester = input()
print()

# 강의목차 => 학기선택
selectSemester = Select(driver.find_element_by_id('term_cd'))

if semester == '1학기':
    selectSemester.select_by_value("10")
if semester == '2학기':
    selectSemester.select_by_value("20")
if semester == '여름 계절학기':
    selectSemester.select_by_value("11")
if semester == '겨울 계절학기':
    selectSemester.select_by_value("21")

# 탐색버튼 클릭
driver.find_element_by_id('ing').click()

# 수강 강의 목록 체크
while (True):
    try:
        driver.find_element_by_xpath("//*/table/tbody/tr[%s]" %courseRow)
        courseRow += 1
    except:
        break

# 수강 강의 목록 출력 (예: 네트워크 시뮬레이션, 모의 해킹, 패킷 분석 툴 활용 등)
while courseIndex < courseRow:
    print("강의번호 : [ %s ] - " %courseIndex + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[4]/span" %courseIndex).text)
    courseIndex += 1

# 강의명 입력
courseNumber = input('\n강의번호 입력 : ')
print()

# 강의 선택
try:
    driver.find_element_by_xpath("//*/table/tbody/tr[" + courseNumber + "]/td[7]/a").click()
except:
    print("출력된 강의 중 원하는 강의번호 입력")

# 강의실 입장 => 강의실 입장
driver.find_element_by_id('/lms/class/courseSchedule/doListView.dunet').click()

# 현재 실행중인 브라우저 탭 핸들 저장
window_before = driver.window_handles[0]

# 강의실 영상 테이블 행 탐색
while (True):
    try:
        driver.find_element_by_xpath("//*/table/tbody/tr[%s]" %courseContentsRow)
        courseContentsRow += 1
    except:
        break

while courseContentsIndex < courseContentsRow:
    #Cyber
    if(driver.find_element_by_xpath('//*[@id="con"]/p[2]').text == "학습환경점검"):
        try:
            print( "[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[2]" %courseContentsIndex).text + " ]", end='')
            print( "[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[3]" %courseContentsIndex).text + " ]", end='')
            print( "[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[6]" %courseContentsIndex).text + " ]")

            if ((driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[6]" %courseContentsIndex).text == "미진행") or (driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[6]" %courseContentsIndex).text[0:3] == "진행중")) and (driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[7]/a/span" %courseContentsIndex).text == "강의보기"):
                driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[7]/a/span" %courseContentsIndex).click() #강의보기 클릭
                time.sleep(120 + 60 * int(driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[3]" %courseContentsIndex).text.replace("분", ""))) #강의시간만큼 대기
                window_after = driver.window_handles[1]
                
                #handle swaping
                driver.switch_to.window(window_after)
                driver.close() 
                driver.switch_to.window(window_before) 
            courseContentsIndex += 1
            
        except:
#            print("Unexpected error:", sys.exc_info()[0]) #에러문구 삭제
            courseContentsIndex += 1
            print()

    #Flip Learning        
    if(driver.find_element_by_xpath('//*[@id="con"]/p[2]').text == "Flipped Learnig 교과목"):
        try:#암호프로그래밍
            if(driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[4]" %courseContentsIndex).text == "Pre"  or  driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[1]" %courseContentsIndex).text == "Pre"):
                if(driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[4]" %courseContentsIndex).text == "Pre"):
                    print("[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[4]" %courseContentsIndex).text + " ]", end='') # 수업방식 (ln / pre pre일 때만 영상 있음)
                    print("[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[5]" %courseContentsIndex).text + " ]", end='') # 수업제목
                    print("[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[6]" %courseContentsIndex).text + " ]", end='') # 출석기간
                    print("[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[8]" %courseContentsIndex).text + " ]") # 진행현황 (완료 / 미진행 / 진행중)
                    if(((driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[8]" %courseContentsIndex).text == "미진행" or driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[8]" %courseContentsIndex).text[0:3] == "진행중")) and driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[4]" %courseContentsIndex).text != "-") :
                        driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[7]" %courseContentsIndex).click()
                        time.sleep(10)
                        window_after = driver.window_handles[1]
                        driver.switch_to.window(window_after)
                        time.sleep(3000)
                        # 페이지에서 재생버튼 클릭 
                        #왼쪽 하단의 시간 정보 겟
                        # 강의시간만큼 타임슬립
                        driver.close() #강의 종료
                        driver.switch_to.window(window_before) #핸들 다시 바꾸기
                    #모의해킹
                if(driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[1]" %courseContentsIndex).text == "Pre"):
                    print("[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[1]" %courseContentsIndex).text + " ]", end='') # 수업방식 (ln / pre pre일 때만 영상 있음)
                    print("[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[2]" %courseContentsIndex).text + " ]", end='') # 수업제목
                    print("[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[3]" %courseContentsIndex).text + " ]", end='') # 출석기간
                    print("[ " + driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[5]" %courseContentsIndex).text + " ]") # 진행현황 (완료 / 미진행 / 진행중)
                    if(((driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[5]" %courseContentsIndex).text == "미진행" or driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[5]" %courseContentsIndex).text[0:3] == "진행중")) and driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[4]" %courseContentsIndex).text != "-") :
                        driver.find_element_by_xpath("//*/table/tbody/tr[%s]/td[4]" %courseContentsIndex).click()
                        time.sleep(10)
                        window_after = driver.window_handles[1]
                        driver.switch_to.window(window_after)
                        time.sleep(3000)
                        # 페이지에서 재생버튼 클릭 
                        # 왼쪽 하단의 시간 정보 겟
                        # 강의시간만큼 타임슬립
                        driver.close() #강의 종료
                        driver.switch_to.window(window_before) #핸들 다시 바꾸기
            courseContentsIndex += 1
        except:
#            print("Unexpected error:", sys.exc_info()[0])
            courseContentsIndex += 1
