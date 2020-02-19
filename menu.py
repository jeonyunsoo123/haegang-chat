import requests, re, json, sys, time

officeCode="stu.pen.go.kr" ## 교육청 코드
schulCode="C100001908" ## 학교 고유코드
schulCrseCode="4" ## 학교 분류코드 (고등학교, 중학교, 초등학교)
schulKndScCode="04" ## 학교 분류코드
schYm="201904"#time.strftime("%Y%m",time.localtime())

##neis web requests
URL="https://" + officeCode + "/sts_sci_md00_001.do"
##params = {'schulCode': 'B100000593', 'schulCrseScCode': '4', 'schulKndScCode' : '04', 'ay' : str(year)}
params = {'schulCode': str(schulCode), 'schulCrseScCode': str(schulCrseCode), 'schulKndScCode' : str(schulKndScCode), 'schYm' : str(schYm)}
response = requests.get(URL, params=params).text
data = response[response.find("<tbody>"):response.find("</tbody>")]

## re 정규표현식으로 불필요한 데이터를 자르거나 변환
regex = re.compile(r'[\n\r\t]')
data=regex.sub('',data)
rex = re.compile(r'<div>(.*?)</div>', re.S|re.M)
data=rex.findall(data)

file_json={}
for dat in data:
    date=re.findall(r"[0-3][0-9]",dat[0:2])
    menu=dat[dat.find("[중식]<br />"):]
    if not date:
        date=dat[0:1]
        if date == "" or date == " ":
            continue
    if type(date) == list:
        date=date[0]
    menu = menu.split("<br />")
    menu.remove(menu[0])
    if not menu:
        menu="None"
    file_json.update({date : menu})

##Json 생성
with open('menu.json', 'w', encoding='utf-8') as outfile:
       json.dump(file_json, outfile, sort_keys = False, indent=4, ensure_ascii=0)
