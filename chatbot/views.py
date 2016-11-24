import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import kakao_user
from .parser import *
import re

@csrf_exempt
def keyboard(request):
    response_json = {}
    response_json['type']='buttons'
    response_json['buttons']=['성적 확인하기']
    return HttpResponse(json.dumps(response_json,ensure_ascii=False), content_type=u"application/json; charset=utf-8")
    
@csrf_exempt
def message(request):
    value=json.loads(request.body.decode("utf-8"))
    
    key=value['user_key']
    text=value['type']
    content=value["content"]
    response_json={}
    try:
        user=kakao_user.objects.get(user_key=key)
        #user.step = 0
        #user.save()
    except:
        user=kakao_user(user_key=key)
        user.save()

    if content == '성적 확인하기':
        user.step = 1 # 1단계
        user.save()
        
        response_json={
            "message":{
                "text": str(user.step)+"단계: "+content+" 선택하셨습니다." # 메시지
            },
            "keyboard":{
                "type": "buttons",
                "buttons":[
                    "종합정보시스템 로그인" # 키보드 버튼
                    ]
            }
        }

    elif user.step == 1:
        user.step = 2 # 2단계
        user.save()
        
        response_json={
            "message":{
                "text": str(user.step)+"단계: "+"ID(학번)를 입력해주세요." # 메시지
            },
            "keyboard":{
                "type": "text"
            }
        }
        
        
    elif user.step == 2:
        user.step = 3 # 3단계
        user.hufs_id = content
        user.save()
        
        response_json={
            "message":{
                "text": str(user.step)+"단계: "+"PASSWORD를 입력해주세요."
            }
        }
        
    elif user.step == 3:
        
        user.step = 4
        user.hufs_pwd = content
        user.save()
        
        p = parsing_class()
        a = p.login_check(user.hufs_id,user.hufs_pwd)
        
        if a == 'fail':
            user.step = 1
            user.save()
            
            response_json={
                "message":{
                    "text": "잘못된 로그인입니다."
                    },
                "keyboard":{
                "type": "buttons",
                "buttons":[
                    "종합정보시스템 재로그인" # 키보드 버튼
                    ]
                }
            }
            
        else:
            p.login(user.hufs_id,user.hufs_pwd)
            user.step = 1
            user.save()
            
            response_json={
                "message":{
                    "text": p.user_info1+"\n"+
                            p.user_info2+"\n"+
                            "\n"+
                            "| 영역별 취득학점"+p.today+"\n"+"\n"+
                            "1전공: "+str(p.grade_dict['1전공'])+"\n"+
                            "이중전공: "+str(p.grade_dict['이중전공'])+"\n"+
                            "2전공: "+str(p.grade_dict['2전공'])+"\n"+
                            "교양(실용)외국어 :"+str(p.grade_dict['교외'])+"\n"+
                            "교양: "+str(p.grade_dict['교양'])+"\n"+
                            "부전공: "+str(p.grade_dict['부전공'])+"\n"+
                            "교직: "+str(p.grade_dict['교직'])+"\n"+
                            "자선: "+str(p.grade_dict['자선'])+"\n"+
                            "총취득: "+str(p.grade_dict['총취득'])+"\n"
                            +"\n"
                            "총평점: "+str(p.grade_dict['총평점'])+"\n"+
                            
                            p.user_major_gpa
                            
                            +"\n"+"\n"+
                            "※ 채팅 내용을 삭제하거나, 재로그인하려면 채팅방 퇴장 후 재입장 바랍니다."
                            
                },
                "keyboard":{
                "type": "buttons",
                "buttons":[
                    "종합정보시스템 재로그인" # 키보드 버튼
                    ]
                }
            }
        
    else:
        response_json={
            "message":{
                "text": str(user.step)+"단계: "+content+" 잘못된 로그인 입니다."+"\n"+" * 참고: 현재 베타테스트. 12월 중 정식오픈 예정"
            }
        }
    
    return HttpResponse(json.dumps(response_json,ensure_ascii=False), content_type=u"application/json; charset=utf-8")
    
@csrf_exempt
def reg_friend(request):
    value=json.loads(request.body.decode("utf-8"))
    key=value['user_key']
    user=kakao_user(user_key=key)
    user.save()
    return HttpResponse("")

@csrf_exempt
def del_friend(request,user_key):
    #유저 키 삭제
    # try: 
    #     del_user=kakao_user.objects.get(user_key=user_key)
    #     del_user.delete()
    # finally:
    return HttpResponse("")


@csrf_exempt
def room(request,user_key):
    #채팅방 나감
    
    return HttpResponse("")