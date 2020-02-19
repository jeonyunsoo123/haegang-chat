
import json, time
haksa_today_day = "20"#time.strftime("%d",time.localtime())
menu_today_day = time.strftime("%d",time.localtime())
year=time.strftime("%Y",time.localtime())
month=time.strftime("%m",time.localtime())
day=time.strftime("%d",time.localtime())
total_msg = []
#print("FLAG1")

f = open("send_text.txt", 'w')



total_msg.append("좋은 아침입니다! 학교 갈 준비 되셨나요?")
total_msg.append("")
total_msg.append("해강고등학교 챗봇에서 오늘의 일정을 알려드립니다")
total_msg.append("오늘은" + year +"년 " + month + "월 " + day + "일 이며")

with open('haksa.json',encoding="utf8") as haksa_json:
    haksa_json_data = json.load(haksa_json)
#print("FLAG2")
haksa_json_string = haksa_json_data[haksa_today_day]

#print(haksa_json_string)
#print("FLAG3")

total_msg.append("학사일정으로는 " + haksa_json_string + "이 예정되어 있습니다.")

total_msg.append("")
total_msg.append("오늘의 급식 정보는 다음과 같습니다")
total_msg.append("")
total_msg.append("[중식]")

with open('menu.json', encoding="utf8") as menu_json:
    menu_json_data = json.load(menu_json)

menu_json_string = menu_json_data[menu_today_day]

for i in menu_json_string:
    total_msg.append(i)

total_msg.append("")
total_msg.append("오늘도 화이팅~")
#f.close()

for i in total_msg:
    print(i)

for i in total_msg:
    f.write(i)
    f.write("\n")
f.close()
