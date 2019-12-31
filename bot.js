'use strict'
const School = require('node-school-kr')

const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');
const app = express();

const school = new School()
school.init(School.Type.HIGH, School.Region.BUSAN, 'C100001908')

const sampleAsync = async function() {
  const meal = await school.getMeal()
  const calendar = await school.getCalendar()

  // 오늘 날짜
  console.log(`${meal.month}월 ${meal.day}일`)

  // 오늘 급식 정보
  console.log(meal.today)

  // 이번 달 급식 정보
  console.log(meal)

  // 이번 달 학사일정
  console.log(calendar)

  // 년도와 달을 지정하여 해당 날짜의 데이터를 조회할 수 있습니다.
  const mealCustom = await school.getMeal(2018, 9)
  const calendarCustom = await school.getCalendar(2017, 4)

  console.log(mealCustom)
  console.log(calendarCustom)

  // 년도값 대신 옵션 객체를 전달하여 데이터 수집 가능
  const optionMeal = await school.getMeal({
    year: 2018,
    month: 9,
    default: '급식이 없습니다'
  })
  const optionCalendar = await school.getCalendar({
    // year, month 생략시 현재 시점 기준으로 조회됨
    default: '일정 없는 날'
  })

  console.log(optionMeal)
  console.log(optionCalendar)
}

sampleAsync()

//const calendar = school.getCalendar()

//작은 따옴표 사이에 본인이 받으신 token을 paste합니다.
//나중에 보안을 위해서 따로 setting을 하는 방법을 알려드리겠습니다.
//이 토큰이 포함된 파일을 절대 업로드하거나 github에 적용시키지 마세요.
var PAGE_ACCESS_TOKEN = process.env.PAGE_ACCESS_TOKEN;

app.set('port', (process.env.PORT || 1337));

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get('/', function(req, res) {
    res.send('Hello world');
})


app.get('/webhook', function(req, res) {
    if (req.query['hub.verify_token'] === 'haegangchat') {
        res.send(req.query['hub.challenge']);
    }
    res.send('Error, wrong token');
})

app.post("/webhook", function(req, res) {
    console.log("WEBHOOK GET IT WORKS");
    var data = req.body;
    console.log(data);

    // Make sure this is a page subscription
    if (data.object == 'page') {
        // Iterate over each entry
        // There may be multiple if batched
        data.entry.forEach(function(pageEntry) {
            var pageID = pageEntry.id;
            var timeOfEvent = pageEntry.time;

            // Iterate over each messaging event
            pageEntry.messaging.forEach(function(messagingEvent) {
                if (messagingEvent.optin) {
                    receivedAuthentication(messagingEvent);
                } else if (messagingEvent.message) {
                    receivedMessage(messagingEvent);
                } else if (messagingEvent.postback) {
                    receivedPostback(messagingEvent);
                } else {
                    console.log("Webhook received unknown messagingEvent: ", messagingEvent);
                }
            });
        });

        res.sendStatus(200);
    }
});

function receivedMessage(event) {
  console.log("------------------MESSAGE RECIEVED--------------------");
    var senderId = event.sender.id;
    var content = event.message.text;
    var echo_message = "ECHO : " + content;
    //if(content.includes('중식') || content.includes('점심')){
    //sendTextMessage(senderId, school.getMeal());



   sendTextMessage(senderId, );
}

function receivedPostback(event) {
    console.log("RECEIVED POSTBACK IT WORKS");
    var senderID = event.sender.id;
    var recipientID = event.recipient.id;
    var timeOfPostback = event.timestamp;

    var payload = event.postback.payload;

    console.log("Received postback for user %d and page %d with payload '%s' " +
        "at %d", senderID, recipientID, payload, timeOfPostback);

    sendTextMessage(senderID, "Postback called");
}

function sendTextMessage(recipientId, message) {
    request({
        url: 'https://graph.facebook.com/v2.6/me/messages',
        qs: { access_token: PAGE_ACCESS_TOKEN },
        method: 'POST',
        json: {
            recipient: { id: recipientId },
            message: { text: message }
        }
    }, function(error, response, body) {
        if (error) {
            console.log('Error sending message: ' + response.error);
        }
    });
}

app.listen(app.get('port'), function() {
    console.log('running on port', app.get('port'));
})
