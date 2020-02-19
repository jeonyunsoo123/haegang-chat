import random
from flask import Flask, request
from pymessenger.bot import Bot
import json, time

app = Flask(__name__)       # Initializing our Flask application
ACCESS_TOKEN = 'EAARPvFZB8vQgBALLAZBukOiIcig039LcVitddt1coru1ehE9am6oK54rTRCELOEkFFzahXtXZBPYdPdZBs8JgK7yzulOrzIvITpAvlDSgV2TwrD0vvlNOdUIncpP1V8rQxBfy8ufv0A6ub2LeZB2mXvEAnu4WZAwaBZBcuZCTMaLIAZDZD'
VERIFY_TOKEN = 'JEONYSTOKEN'
bot = Bot('EAARPvFZB8vQgBALLAZBukOiIcig039LcVitddt1coru1ehE9am6oK54rTRCELOEkFFzahXtXZBPYdPdZBs8JgK7yzulOrzIvITpAvlDSgV2TwrD0vvlNOdUIncpP1V8rQxBfy8ufv0A6ub2LeZB2mXvEAnu4WZAwaBZBcuZCTMaLIAZDZD')

haksa_today_day = "20"#time.strftime("%d",time.localtime())
menu_today_day = time.strftime("%d",time.localtime())
year=time.strftime("%Y",time.localtime())
month=time.strftime("%m",time.localtime())
day=time.strftime("%d",time.localtime())
total_msg = []
#print("FLAG1")

f = open("send_text.txt", 'w', encoding="utf8")

total_msg.append("좋은 아침입니다! 학교 갈 준비 되셨나요?")
total_msg.append("")
total_msg.append("해강고등학교 챗봇에서 오늘의 일정을 알려드립니다")
total_msg.append("오늘은" + year +"년 " + month + "월 " + day + "일 이며")

with open('haksa.json',encoding="utf8") as haksa_json:
    haksa_json_data = json.load(haksa_json)
#print("FLAG2")
haksa_json_string = haksa_json_data[haksa_today_day]

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




# Importing standard route and two requst types: GET and POST.
# We will receive messages that Facebook sends our bot at this endpoint
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Before allowing people to message your bot Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook.
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # If the request was not GET, it  must be POSTand we can just proceed with sending a message
    # back to user
    else:
            # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    # if user send us a GIF, photo, video or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_text =get_message()
                        send_message(recipient_id, response_sent_text)
    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by Facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def get_message():

    sample_responses = ["You are stunning!", "We're proud of you",
                        "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    #return random.choice(sample_responses)
    return "\n".join(total_msg)


# Uses PyMessenger to send response to the user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


# Add description here about this if statement.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
