from fastapi import FastAPI, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, ImageMessage
from module import globals, functions
import os

# 初始化 FastAPI
app = FastAPI()

# 設定 Line Bot API 及 Webhook Handler
channel_access_token = "token123321"
channel_secret = "secret789"
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# 初始化變數
globals.init()


@app.get("/original_image")
async def original_image():
    image_path = os.path.join('static', 'image', globals.original_image_filename)
    return {"upload_image": image_path}


@app.get("/preview_image")
async def preview_image():
    image_path = os.path.join('static', 'image', globals.preview_image_filename)
    return {"upload_image": image_path}


@app.post("/callback")
async def callback(request: Request):
    # Get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature')

    # Get request body as bytes
    body = await request.body()

    # Handle webhook body
    try:
        body_text = body.decode("utf-8")
        handler.handle(body_text, signature)
        print(body_text)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid Signature")

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    message = None
    globals.users = functions.add_user(users=globals.users, user_id=user_id)  # 新增 user id 如果 user id 不在 users 的 key

    if event.message.text == '小幫手':
        print(f"[小幫手] stage 0 event = {event}")
        print(f"[小幫手] stage 0 users = {globals.users.keys()}")
        # 變數初始化
        globals.users = functions.initialize(users=globals.users, user_id=user_id)
        # 回傳訊息
        message = functions.BotMessage.helper_menu()
        # 進入下一個 stage
        globals.users[user_id]['stage'] = 1
    elif globals.users[user_id]['stage'] == 1:
        if event.message.text == globals.service_list[0]:
            print(f"[{event.message.text}] stage 1 event = {event}")
            print(f"[{event.message.text}] stage 1 users = {globals.users.keys()}")
            # 儲存服務項目
            globals.users[user_id]['service'] = event.message.text
            # 回傳訊息
            message = list()
            message.append(functions.BotMessage.text_message(content="很高興為您服務"))
            message.append(functions.BotMessage.anomaly_type())
            # 進入下一個 stage
            globals.users[user_id]['stage'] = 2
        elif event.message.text == globals.service_list[1]:
            pass
        elif event.message.text == globals.service_list[2]:
            pass
        elif event.message.text == globals.service_list[3]:
            pass
        else:
            # 回傳訊息
            message = list()
            message.append(functions.BotMessage.text_message(content="目前尚未提供此服務"))
            message.append(functions.BotMessage.text_message(content="請重新選擇服務項目"))
            message.append(functions.BotMessage.helper_menu())
    elif globals.users[user_id]['stage'] == 2:
        if globals.users[user_id]['service'] == globals.service_list[0]:
            if event.message.text in globals.anomaly_type_list:
                print(f"[{globals.users[user_id]['service']}] stage 2 event = {event}")
                print(f"[{globals.users[user_id]['service']}] stage 2 users = {globals.users.keys()}")
                # 儲存回報的異常類型
                globals.users[user_id]['anomaly_type'] = event.message.text
                # 回傳訊息
                message = list()
                content = f"好的，您選擇回報的異常類型是「{globals.users[user_id]['anomaly_type']}」"
                message.append(functions.BotMessage.text_message(content=content))
                if not globals.users[user_id]['modify']:
                    message.append(functions.BotMessage.anomaly_datetime())
                else:
                    ret_message = functions.BotMessage.confirm_work_order(user_id=user_id,
                                                                          content="請確認更新過後的工單資訊是否正確")
                    for mes in ret_message:
                        message.append(mes)
                # 進入下一個 stage
                globals.users[user_id]['stage'] = 3 if not globals.users[user_id]['modify'] else 6
            else:
                # 回傳訊息
                message = list()
                message.append(functions.BotMessage.text_message(content="目前無此異常類型"))
                message.append(functions.BotMessage.anomaly_type(content="請重新選擇異常類型"))
        elif globals.users[user_id]['service'] == globals.service_list[1]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[2]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[3]:
            pass
    elif globals.users[user_id]['stage'] == 4:
        if globals.users[user_id]['service'] == globals.service_list[0]:
            if globals.users[user_id]['anomaly_type'] in globals.anomaly_type_list:
                print(f"[{globals.users[user_id]['service']}] stage 4 event = {event}")
                print(f"[{globals.users[user_id]['service']}] stage 4 users = {globals.users.keys()}")
                # 儲存簡述的異常問題
                globals.users[user_id]['anomaly_brief'] = event.message.text
                # 回傳訊息
                message = list()
                content = f"好的，您簡述的問題為「{globals.users[user_id]['anomaly_brief']}」"
                message.append(functions.BotMessage.text_message(content=content))
                if not globals.users[user_id]['modify']:
                    message.append(functions.BotMessage.anomaly_detail())
                else:
                    ret_message = functions.BotMessage.confirm_work_order(user_id=user_id,
                                                                          content="請確認更新過後的工單資訊是否正確")
                    for mes in ret_message:
                        message.append(mes)
                # 進入下一個 stage
                globals.users[user_id]['stage'] = 5 if not globals.users[user_id]['modify'] else 6
        elif globals.users[user_id]['service'] == globals.service_list[1]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[2]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[3]:
            pass
    elif globals.users[user_id]['stage'] == 5:
        if globals.users[user_id]['service'] == globals.service_list[0]:
            if globals.users[user_id]['anomaly_type'] in globals.anomaly_type_list:
                print(f"[{globals.users[user_id]['service']}] stage 5 event = {event}")
                print(f"[{globals.users[user_id]['service']}] stage 5 users = {globals.users.keys()}")
                # 儲存詳述的異常狀況
                globals.users[user_id]['anomaly_detail'] = event.message.text
                # 回傳訊息
                message = list()
                content = f"好的，您詳述的狀況為「{globals.users[user_id]['anomaly_detail']}」"
                message.append(functions.BotMessage.text_message(content=content))
                if not globals.users[user_id]['modify']:
                    ret_message = functions.BotMessage.confirm_work_order(user_id=user_id)
                else:
                    ret_message = functions.BotMessage.confirm_work_order(user_id=user_id,
                                                                          content="請確認更新過後的工單資訊是否正確")
                for mes in ret_message:
                    message.append(mes)
                # 進入下一個 stage
                globals.users[user_id]['stage'] = 6
        elif globals.users[user_id]['service'] == globals.service_list[1]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[2]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[3]:
            pass
    elif globals.users[user_id]['stage'] == 6:
        if globals.users[user_id]['service'] == globals.service_list[0]:
            if globals.users[user_id]['anomaly_type'] in globals.anomaly_type_list:
                print(f"[{globals.users[user_id]['service']}] stage 6 event = {event}")
                print(f"[{globals.users[user_id]['service']}] stage 6 users = {globals.users.keys()}")
                if event.message.text == globals.confirm_yes:
                    # 回傳訊息
                    message = list()
                    message.append(functions.BotMessage.text_message(content="工單已建立完成"))
                    message.append(functions.BotMessage.text_message(content="感謝您的填寫"))
                    # 變數初始化
                    globals.users = functions.initialize(users=globals.users, user_id=user_id)
                elif event.message.text == globals.confirm_no:
                    # 回傳訊息
                    message = functions.BotMessage.anomaly_modify_item()
                    # 進入修改的 stage
                    globals.users[user_id]['stage'] = -1
                    globals.users[user_id]['modify'] = True
                else:
                    # 回傳訊息
                    message = list()
                    content = f"目前僅提供\"{globals.confirm_yes}\"和\"{globals.confirm_no}\"兩個選項"
                    message.append(functions.BotMessage.text_message(content=content))
                    ret_message = functions.BotMessage.confirm_work_order(user_id=user_id,
                                                                          content="請重新選擇確認工單資訊是否正確")
                    for mes in ret_message:
                        message.append(mes)
        elif globals.users[user_id]['service'] == globals.service_list[1]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[2]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[3]:
            pass
    elif globals.users[user_id]['stage'] == -1:
        if globals.users[user_id]['service'] == globals.service_list[0]:
            print(f"[{globals.users[user_id]['service']}] stage -1 event = {event}")
            print(f"[{globals.users[user_id]['service']}] stage -1 users = {globals.users.keys()}")
            if event.message.text == globals.anomaly_modify_list[0]:
                # 回傳訊息
                message = functions.BotMessage.anomaly_type(content="請重新選擇您要回報的異常類型")
                # 進入 stage 2
                globals.users[user_id]['stage'] = 2
            elif event.message.text == globals.anomaly_modify_list[1]:
                # 回傳訊息
                message = functions.BotMessage.anomaly_datetime(content="請重新選擇異常回報的時間")
                # 進入 stage 3
                globals.users[user_id]['stage'] = 3
            elif event.message.text == globals.anomaly_modify_list[2]:
                # 回傳訊息
                message = functions.BotMessage.anomaly_brief(content="請重新\"簡述\"異常問題為何 (此為工單標題)")
                # 進入 stage 4
                globals.users[user_id]['stage'] = 4
            elif event.message.text == globals.anomaly_modify_list[3]:
                # 回傳訊息
                message = functions.BotMessage.anomaly_detail(content="請重新\"詳述\"異常的狀況 (此為工單內容)")
                # 進入 stage 5
                globals.users[user_id]['stage'] = 5
            else:
                # 回傳訊息
                message = list()
                message.append(functions.BotMessage.text_message(content="目前尚未提供修改此項目"))
                message.append(functions.BotMessage.anomaly_modify_item(content="請重新選擇要修改的項目"))
        elif globals.users[user_id]['service'] == globals.service_list[1]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[2]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[3]:
            pass
    else:
        # 回傳訊息
        message = functions.BotMessage.text_message(content="請輸入「小幫手」以選擇服務項目")

    line_bot_api.reply_message(event.reply_token, message)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    user_id = event.source.user_id
    # message = None
    globals.users = functions.add_user(users=globals.users, user_id=user_id)  # 新增 user id 如果 user id 不在 users 的 key

    # 用 message id 拿取 message content，並將 image 儲存於 local server
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id=message_id)
    file_path = os.path.join('static', 'image', f"{user_id}_temp.jpg")
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    # 將 image resize 至符合 Line Developers 規範的大小，再把 resized image 儲存於 local server
    original_file_path = os.path.join('static', 'image', f"{user_id}_{globals.original_image_filename}")
    preview_file_path = os.path.join('static', 'image', f"{user_id}_{globals.preview_image_filename}")
    functions.resize_and_save_image(src_file=file_path, dst_file=original_file_path, category='original')
    functions.resize_and_save_image(src_file=file_path, dst_file=preview_file_path, category='preview')
    # 回傳訊息
    ret_message = list()
    ret_message.append(functions.BotMessage.text_message(content="您傳送的圖片如下"))
    ret_message.append(functions.BotMessage.image_message(user_id=user_id))

    print(f"image message event = {event}")
    print(f"image message id = {message_id}")
    print(f"image message content = {message_content}")

    line_bot_api.reply_message(event.reply_token, ret_message)


@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    message = None

    if globals.users[user_id]['stage'] == 3:
        if globals.users[user_id]['service'] == globals.service_list[0]:
            if globals.users[user_id]['anomaly_type'] in globals.anomaly_type_list:
                print(f"[{globals.users[user_id]['service']}] stage 3 event = {event}")
                print(f"[{globals.users[user_id]['service']}] stage 3 users = {globals.users.keys()}")
                # 儲存異常回報的時間
                anomaly_datetime = event.postback.params['datetime']
                globals.users[user_id]['anomaly_datetime'] = anomaly_datetime.replace('T', ' ')
                # 回傳訊息
                message = list()
                content = f"好的，您選擇的異常回報時間為「{globals.users[user_id]['anomaly_datetime']}」"
                message.append(functions.BotMessage.text_message(content=content))
                if not globals.users[user_id]['modify']:
                    message.append(functions.BotMessage.anomaly_brief())
                else:
                    ret_message = functions.BotMessage.confirm_work_order(user_id=user_id,
                                                                          content="請確認更新過後的工單資訊是否正確")
                    for mes in ret_message:
                        message.append(mes)
                # 進入下一個 stage
                globals.users[user_id]['stage'] = 4 if not globals.users[user_id]['modify'] else 6
        elif globals.users[user_id]['service'] == globals.service_list[1]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[2]:
            pass
        elif globals.users[user_id]['service'] == globals.service_list[3]:
            pass

    line_bot_api.reply_message(event.reply_token, message)
