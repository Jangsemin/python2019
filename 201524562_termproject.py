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
