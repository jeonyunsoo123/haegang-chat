import json, time
haksa_today_day = time.strftime("%d",time.localtime())
menu_today_day = "1"

with open('haksa.json') as haksa_json:
    haksa_json_data = json.load(haksa_json)

haksa_json_string = haksa_json_data[haksa_today_day]

print(haksa_json_string)


with open('menu.json') as menu_json:
    menu_json_data = json.load(menu_json)

menu_json_string = menu_json_data[menu_today_day]



print(menu_json_string)
