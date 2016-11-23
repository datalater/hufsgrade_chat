from .models import kakao_user

import os
import sys

import requests
from bs4 import BeautifulSoup
import re
import time
#from os.path import join, abspath

head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
login_url = "https://webs.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp"
main_page = "http://webs.hufs.ac.kr:8989/src08/jsp/main.jsp?"
studentinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/stuinfo_10/STUINFO1000C_myinfo.jsp"
credits_url = "http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_Top.jsp?tab_lang=K"
credits_list_url = "http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_List.jsp?tab_lang=K"


class parsing_class():

    # def __init__(self):
    #     user_id = input("아이디를 입력하세요: ")
    #     user_pwd = input("비밀번호를 입력하세요: ")
    
    def login_check(self,user_id,user_pwd):
        
        #-------------------------로그인 성공 여부 체크--------------------------#
        
        self.current_session = requests.session()
        params = {'user_id': user_id,'password': user_pwd,'gubun': 'o','reurl': '','SSL_Login': 1}
        
        self.current_session.post(login_url, data=params, headers=head)
        
        #-------------------------학생정보--------------------------#
        
        self.current_session.get(main_page, headers=head)

        self.studentinfo = self.current_session.get(studentinfo_url, headers=head)
        html = BeautifulSoup(self.studentinfo.text, "html.parser")

        student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
        try:
            student_major = student_college.next_element.next_element.next_element.next_element.string
        except AttributeError:
            error_message = "잘못된 로그인입니다."
            
        return error_message
        
    def login(self,user_id,user_pwd):
    
        self.current_session = requests.session()
        params = {'user_id': user_id,'password': user_pwd,'gubun': 'o','reurl': '','SSL_Login': 1}
        
        self.current_session.post(login_url, data=params, headers=head)
        
        #-------------------------학생정보--------------------------#
        self.current_session.get(main_page, headers=head)

        self.studentinfo = self.current_session.get(studentinfo_url, headers=head)
        html = BeautifulSoup(self.studentinfo.text, "html.parser")

        student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
        try:
            student_major = student_college.next_element.next_element.next_element.next_element.string
        except AttributeError:
            error_message = "잘못된 로그인입니다."
            
        #student_id= html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
        student_id = user_id
        student_name = html.find(string=re.compile('성명')).parent.parent.next_sibling.next_element.next_element.next_element.next_sibling.next_sibling.string
        student_name = student_name.replace("\r\n\t\t\t\t","")
        student_name_ko = html.find(string=re.compile('성명')).parent.next_sibling.next_sibling.next_sibling.next_sibling.string

        
        # 입학연도 
        student_id_year = int(str(student_id)[:4])
        
        
        #-------------------------성적정보(영역별취득학점)--------------------------#

        self.graduateinfo=self.current_session.get(credits_url,headers=head)
        html = BeautifulSoup(self.graduateinfo.text, "html.parser")
        
        # 이중전공자 전공심화자 구분 및 각 전공 과목 parsing
        major_state = ""
        if html.find(string=re.compile('\[이중전공\]')) is not None:
            major_state ="이중전공"
            student_other_major = html.find(string=re.compile('\[이중전공\]')).next_element
            student_other_major = student_other_major.replace(u'\xa0', u' ').replace("(","").replace(" ","")
            student_other_major = "이중: " + student_other_major
        elif html.find(string=re.compile('전공심화')) is not None:
            major_state = "전공심화(부전공)"
            student_other_major = html.find(string=re.compile('전공심화')).next_element
            student_other_major = student_other_major.replace(u'\xa0', u' ').replace("(","").replace(" ","")
            student_other_major = "부:" + student_other_major
        else:
            major_state = "not yet decided"
        
        # 1전공 parsing
        student_first_major = html.find(string=re.compile('\[1전공\]')).next_element
        student_first_major = student_first_major.replace(u'\xa0', u' ').replace("(","").replace(" ","")

        grade_name = [i.string for i in html.find("tr",class_="table_gray4").find_all("td")]
        if '실외' in grade_name:
            index_number = grade_name.index('실외')
            grade_name[index_number] = '교외'

        grade_data = [i.string for i in html.find("tr",class_="table_w").find_all("td")]
        credits_completed = grade_data[1:-2]
        grade_per_average = grade_data[-2:]
                        
        graduateinfo = credits_completed + grade_per_average
        
        #2015~학번(사범대 제외)
        dual_major_required_15 = [54, 42, 0, 6, 26, 0, 0, 6, 134, 4.5]
        minor_required_15         = [70, 0, 21, 6, 26, 0, 0, 11, 134, 4.5]
        dual_major_required_15 = list(map(str, dual_major_required_15))
        minor_required_15         = list(map(str, minor_required_15))
        
        #2007~2014학번(사범대 제외)
        dual_major_required  = [54, 54, 0, 4, 22, 0, 0, 0, 134, 4.5]
        minor_required          = [75, 0, 0, 4, 22, 21, 0, 12, 134, 4.5]
        dual_major_required = list(map(str, dual_major_required))
        minor_required = list(map(str, minor_required))


        self.grade_dict = dict()
        for i in range(len(grade_name)):
            self.grade_dict[grade_name[i]] = grade_data[i]





        #-------------------------성적정보(전공평점)--------------------------#

        self.creditsinfo=self.current_session.get(credits_list_url,headers=head)
        html = BeautifulSoup(self.creditsinfo.text, "html.parser")

        grade_dic = {'A+':4.5, 'A0':4.0, 'B+':3.5, 'B0':3.0, 'C+':2.5, 'C0':2.0, 'D+':1.5, 'D0':1.0, 'F':0}

        # 전공 평점 구하기 시작
        first_major_credit = [] # credit: 학점(e.g. 3)
        first_major_grade = [] # grade: 등급(e.g. A+)
        first_major_grade_float = [] # grade_float: 등급 환산 점수(e.g. A+ -> 4.5)
        first_major_multiply = []
        
        for td in html.find_all("tr",class_="table_w"):
            for td_first_major in td.find_all(string=re.compile('1전공|이중')):
                for td_grades in td_first_major.parent.next_sibling.next_sibling.next_sibling.next_sibling:
                    if not td_grades == 'PASS':
                        first_major_grade.append(td_grades)
                        for td_credits in td_first_major.parent.next_sibling.next_sibling:
                            first_major_credit.append(float(td_credits))

        # 등급 점수로 환산하기(e.g. A+ -> 4.5)
        for element in first_major_grade:
            first_major_grade_float.append(grade_dic[element])

        
        # 학점 곱하기 등급
        for i in range(len(first_major_credit)):
            first_major_multiply.append(first_major_credit[i] * first_major_grade_float[i])

        # 전공 평점 구하기 끝
        first_major_gpa = round(sum(first_major_multiply)/sum(first_major_credit),2)
        
        
        
        #-------------------------학생정보 나타내기--------------------------#

        self.user_info1 = student_id + " " + student_first_major + "(" + student_other_major + ")"
        self.user_info2 = student_name_ko+"("+student_name+")"+"님, 반갑습니다."
        
        print(self.user_info1)
        print(self.user_info2)

            
        self.user_major_gpa = "(전공평점: "+str(first_major_gpa)+")"
        print(self.grade_dict)
        print(self.user_major_gpa)

        #-----------------------------------------------------------------------------------#
