# 본인의 과제명 작성

학과 | 학번 | 성명
---- | ---- | ---- 
정보컴퓨터공학부 |201524562 |장세민


## 프로젝트 개요
부산광역시 공공부문(공공기관, 공사기관, 출자출연기관, 대학 등) 일자리(채용)정보를 받아와서 데이터 분석. 지원자가 채용분야, 근무형태, 근무지역 등의 희망하는 채용정보를 입력하면 그에 적합한 일자리를 추천해주는 프로그램 구현.

Json 파싱 - 채용분야, 근무기간, 근무지역, 지원방법, 접수시작일, 접수마감일

![json_data](https://user-images.githubusercontent.com/37135325/59245595-70419b00-8c54-11e9-9fee-0ebe28964ed5.PNG)

실행화면1 - 전체 채용정보 한번에 파이스크립터에 출력

![execute1](https://user-images.githubusercontent.com/37135325/59245236-c01f6280-8c52-11e9-9f82-3e6216955b6e.PNG)

실행화면2 - 지원자의 희망 구직 정보를 입력받아 적합한 채용 정보만 출력  

![execute2](https://user-images.githubusercontent.com/37135325/59245234-bf86cc00-8c52-11e9-9f23-bd2d9ea9bffe.PNG)

데이터 csv 파일 - Json파일 데이터 출력을 깔끔하게 보기 위해서 엑셀 파일에 전체 채용정보 저장

![execute3](https://user-images.githubusercontent.com/37135325/59245235-bf86cc00-8c52-11e9-9561-6b798ed0fe22.PNG)

<간단한 구현 동영상>

<iframe width="560" height="315" src="https://www.youtube.com/embed/UbPN4BWGYvc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



## 사용한 공공데이터 
[데이터보기](http://apis.data.go.kr/6260000/BusanJobOpnngInfoService/getJobOpnngInfo?serviceKey=c071zsOCnJh%2BmGSOdQYopb5%2FBiRaS5K7s1bDzse5MSqvc5ML2X1bnCe0Cv24OXlj2tSwPzddXNFcN%2BtWPEAK7w%3D%3D&pageNo=1&numOfRows=20&resultType=json)
## 소스
* [링크로 소스 내용 보기](https://github.com/cybermin/python2019/blob/master/tes.py) 

* 코드 삽입
~~~python
#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      장세민
#
# Created:     04-06-2019
# Copyright:   (c) 장세민 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib.request
import json
import pandas as pd


jobIdListURL = """http://apis.data.go.kr/6260000/BusanJobOpnngInfoService/getJobOpnngInfo?serviceKey=c071zsOCnJh%2BmGSOdQYopb5%2FBiRaS5K7s1bDzse5MSqvc5ML2X1bnCe0Cv24OXlj2tSwPzddXNFcN%2BtWPEAK7w%3D%3D&pageNo=1&numOfRows=20&resultType=json"""

jobIdpage = urllib.request.urlopen(jobIdListURL)
jobIdData = json.loads(jobIdpage.read())

jobIDDF = pd.DataFrame()
jobIDDF = jobIDDF.append({"title":"", "workDate_nm":"","workregiontxt":"","reqType_nm":"", "reqDate_s":"", "reqDate_e":""}, ignore_index=True)

num = len(jobIdData["getJobOpnngInfo"]["item"])

for i in range(0, num) :
    jobIDDF.ix[i, "title"] = jobIdData["getJobOpnngInfo"]["item"][i]["title"] # 채용 공고 제목 (분야)
    ##print(jobIDDF.ix[i, "title"])
    jobIDDF.ix[i, "workDate_nm"] = jobIdData["getJobOpnngInfo"]["item"][i]["workDate_nm"] # 근무기간(정규직/기간제)
    jobIDDF.ix[i, "workregiontxt"] = jobIdData["getJobOpnngInfo"]["item"][i]["workregiontxt"] # 근무지역(부산)
    jobIDDF.ix[i, "reqType_nm"] = jobIdData["getJobOpnngInfo"]["item"][i]["reqType_nm"] # 지원방법(홈페이지/이메일/방문접수)
    jobIDDF.ix[i, "reqDate_s"] = jobIdData["getJobOpnngInfo"]["item"][i]["reqDate_s"] # 접수시작시간

    if  jobIdData["getJobOpnngInfo"]["item"][i]["reqDate_e"] != []:
        jobIDDF.ix[i, "reqDate_e"] = jobIdData["getJobOpnngInfo"]["item"][0]["reqDate_e"] # 접수마감시간

    else :
        jobIDDF.ix[i,"reqDate_e"] = ""

# 파싱한 json 파일 데이터를 출력을 보기 좋게 하기 위해 csv파일에 write

fp = open("job.csv", "w")

for ads in range(len(jobIDDF)) :
    if ads == 0 :
        for k in jobIDDF.ix[0].keys() : print(k, end=",", file=fp)
        print(file=fp)
    for k in jobIDDF.ix[0].keys() :
        commacut = jobIDDF.ix[ads, k].replace(",", "")
        print(commacut, end=",", file=fp)
    print(file=fp)


fp.close()

#파이스크립터 화면에 전체 json 데이터 출력하기 위함
fp = open("job.csv", "r")

for row in fp :
    elem = row.split(",")
    for string in elem :
        print("%10s" % string, end="\t")
    print()

'''채용 희망 정보 받아와서 적합한 채용 정보 출력
희망 질문 4개 다 맞는 것만  출력. 아닐 시에 다시 입력 유도
'''
jobTitle = input("어떤 관련 직종을 희망하십니까?(EX. 간호사)")
workDate = input("근무기간은 어떻게 희망하십니까까?(정규직 / 기간제)")
workRegion = input("근무 지역은 어디를 희망하십니까?(EX. 부산진구)")
reqType = input("지원 방법은 어떤 것을 선호하십니까?(홈페이지 / 방문접수 / 이메일)")

result = 0
count = 0
for k in range(0, num) :
    if jobTitle in jobIDDF.ix[k, "title"] :
        if workDate in jobIDDF.ix[k, "workDate_nm"] :
            if workRegion in jobIDDF.ix[k, "workregiontxt"] :
                if reqType in jobIDDF.ix[k, "reqType_nm"] :
                    result = 1

    if result == 1 :
        print("귀하에게 적합한 채용 정보를 알려드리겠습니다.")
        print(jobIDDF.ix[k])
        count = 1
        result = 0

if count == 0 :
    print("적합한 채용정보가 없습니다. 다시 입력해보십시오.")

~~~
