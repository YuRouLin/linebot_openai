from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, MemberJoinedEvent
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 用户状态字典，用来存储每个用户的状态
user_state = {}

questions_answers = {
    '球員背號': {
        "0": "道鉑戈",
        "1": "林哲瑄",
        "2": "林澤彬",
        "3": "王勝偉",
        "5": "王念好",
        "6": "葉子霆",
        "7": "陳真",
        "10": "姚冠瑋",
        "11": "蔣智賢",
        "12": "江國豪",
        "14": "王苡丞",
        "18": "黃保羅",
        "21": "藍愷青",
        "22": "李宗賢",
        "23": "布藍登",
        "24": "戈威士",
        "25": "賴智垣",
        "29": "申皓瑋",
        "34": "王蔚永",
        "35": "王正棠",
        "43": "豊瑋",
        "46": "范國宸",
        "48": "岳少華",
        "50": "吳世豪",
        "54": "李建勳",
        "57": "歐書誠",
        "59": "陳冠勳",
        "60": "曾峻岳",
        "64": "羅戈",
        "65": "蔡佳諺",
        "66": "李東洺",
        "67": "辛元旭",
        "69": "張進德",
        "70": "張瑞麟",
        "71": "江少慶",
        "78": "董子恩",
        "80": "游霆崴",
        "81": "陳仕朋",
        "82": "孔念恩",
        "83": "張宥鈞",
        "85": "劉俊豪",
        "87": "富藍戈",
        "95": "戴培峰",
        "97": "池恩齊",
        "98": "高國麟",
    },
    '啦啦隊背號': {
        "0": "蓁蓁",
        "1": "寶兒",
        "6": "奶昔",
        "7": "朱朱",
        "10": "Kesha",
        "15": "丹丹",
        "20": "傑米",
        "23": "Tiffany",
        "24": "秀秀子",
        "25": "安娜",
        "28": "卡洛琳",
        "29": "李雅英",
        "37": "慈妹",
        "51": "李皓禎",
        "58": "大頭",
        "64": "東東",
        "66": "Jessy",
        "77": "維心",
        "90": "栗子",
        "97": "沁沁",
        "6": "南珉貞",
        "100": "檸檬",
    }
}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text.strip()

    if user_id not in user_state:
        user_state[user_id] = None

    if msg == '球員及啦啦隊介紹':
        line_bot_api.reply_message(event.reply_token, TextSendMessage("想查詢球員還是啦啦隊?"))
    elif msg == '球員':
        user_state[user_id] = '球員背號'
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入想查詢的球員背號"))
    elif msg == '啦啦隊':
        user_state[user_id] = '啦啦隊背號'
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入想查詢的啦啦隊背號"))
    else:
        current_state = user_state[user_id]
        if current_state and msg in questions_answers[current_state]:
            reply = questions_answers[current_state][msg]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(reply))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("未找到相關答案，請重新輸入相對應的關鍵字"))

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
