from typing import Dict, List, Any
from linebot.models import TemplateSendMessage, TextSendMessage, ImageSendMessage
from linebot.models import ButtonsTemplate, QuickReply, QuickReplyButton
from linebot.models import URIAction, MessageAction, DatetimePickerAction
from module import globals
import cv2


def add_user(users: Dict[str, Dict[str, Any]], user_id: str) -> Dict[str, Dict[str, Any]]:
    users_copy = users.copy()
    uid = user_id

    # 新增 user id 如果 user id 不在 users 的 key
    if uid not in users_copy:
        users_copy[uid] = dict()
        users_copy = initialize(users=users_copy, user_id=uid)  # 初始化變數

    return users_copy


def initialize(users: Dict[str, Dict[str, Any]], user_id: str) -> Dict[str, Dict[str, Any]]:
    users_copy = users.copy()
    uid = user_id

    # 初始化變數
    users_copy[uid]['stage'] = 0
    users_copy[uid]['modify'] = False
    users_copy[uid]['service'] = None
    users_copy[uid]['anomaly_type'] = None
    users_copy[uid]['anomaly_datetime'] = None
    users_copy[uid]['anomaly_brief'] = None
    users_copy[uid]['anomaly_detail'] = None

    return users_copy


def resize_and_save_image(src_file: str, dst_file: str, category: str):
    image = cv2.imread(src_file)
    height, width = image.shape[:2]
    horizontal = True if width >= height else False
    target_pixel = 1024 if category == 'original' else 240 if category == 'preview' else 128

    # 寬度 >= 長度
    if horizontal:
        # 不需要 resize
        if width <= target_pixel:
            cv2.imwrite(dst_file, image)
            return None
        # 做 resize
        ratio = target_pixel / width
        resized_width, resized_height = int(width * ratio), int(height * ratio)
        resized_image = cv2.resize(image, (resized_width, resized_height), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(dst_file, resized_image)
    # 寬度 < 長度
    else:
        # 不需要 resize
        if height <= target_pixel:
            cv2.imwrite(dst_file, image)
            return None
        # 做 resize
        ratio = target_pixel / height
        resized_width, resized_height = int(width * ratio), int(height * ratio)
        resized_image = cv2.resize(image, (resized_width, resized_height), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(dst_file, resized_image)

    return None


class BotMessage(object):
    @staticmethod
    def helper_menu() -> TemplateSendMessage:
        alt_text = f"您好，這裡是SWT工單系統，小幫手將協助您建立工單服務，請從以下輸入您的需求：" \
                   f"(1).{globals.service_list[0]}；(2).{globals.service_list[1]}；" \
                   f"(3).{globals.service_list[2]}；(4).{globals.service_list[3]}。"
        title = "請選擇服務項目"
        text = "您好，這裡是SWT工單系統，小幫手將協助您建立工單服務，請從下列選項中選擇您的需求。"
        image_url = "https://t3.ftcdn.net/jpg/05/39/63/88/360_F_539638813_CcdRx5ZDVR5pkEB35iDn7qVxtNCiRrRN.jpg"
        message = TemplateSendMessage(
            alt_text=alt_text,
            template=ButtonsTemplate(
                thumbnail_image_url=image_url,
                title=title,
                text=text,
                default_action=URIAction(label="image", uri=image_url),
                actions=[
                    MessageAction(
                        label=globals.service_list[0],
                        text=globals.service_list[0]
                    ),
                    MessageAction(
                        label=globals.service_list[1],
                        text=globals.service_list[1]
                    ),
                    MessageAction(
                        label=globals.service_list[2],
                        text=globals.service_list[2]
                    ),
                    MessageAction(
                        label=globals.service_list[3],
                        text=globals.service_list[3]
                    )
                ]
            )
        )
        return message

    @staticmethod
    def anomaly_type(content: str = None) -> TextSendMessage:
        text = "請選擇您要回報的異常類型" if content is None else content
        message = TextSendMessage(
            text=text,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(
                            label=globals.anomaly_type_list[0],
                            text=globals.anomaly_type_list[0]
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label=globals.anomaly_type_list[1],
                            text=globals.anomaly_type_list[1]
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label=globals.anomaly_type_list[2],
                            text=globals.anomaly_type_list[2]
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label=globals.anomaly_type_list[3],
                            text=globals.anomaly_type_list[3]
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label=globals.anomaly_type_list[4],
                            text=globals.anomaly_type_list[4]
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label=globals.anomaly_type_list[5],
                            text=globals.anomaly_type_list[5]
                        )
                    )
                ]
            )
        )
        return message

    @staticmethod
    def anomaly_datetime(content: str = None) -> TextSendMessage:
        text = "請選擇異常回報的時間" if content is None else content
        label = "選擇日期與時間"
        data = "storeId=12345"
        mode = "datetime"
        message = TextSendMessage(
            text=text,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=DatetimePickerAction(label=label, data=data, mode=mode)
                    )
                ]
            )
        )
        return message

    @staticmethod
    def anomaly_brief(content: str = None) -> TextSendMessage:
        text = "請\"簡述\"異常問題為何 (此為工單標題)" if content is None else content
        message = TextSendMessage(text=text)
        return message

    @staticmethod
    def anomaly_detail(content: str = None) -> TextSendMessage:
        text = "請\"詳述\"異常的狀況 (此為工單內容)" if content is None else content
        message = TextSendMessage(text=text)
        return message

    @staticmethod
    def anomaly_modify_item(content: str = None) -> TextSendMessage:
        text = "請選擇要修改的項目" if content is None else content
        message = TextSendMessage(
            text=text,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(
                            label=globals.anomaly_modify_list[0],
                            text=globals.anomaly_modify_list[0]
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label=globals.anomaly_modify_list[1],
                            text=globals.anomaly_modify_list[1]
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label=globals.anomaly_modify_list[2],
                            text=globals.anomaly_modify_list[2]
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label=globals.anomaly_modify_list[3],
                            text=globals.anomaly_modify_list[3]
                        )
                    )
                ]
            )
        )
        return message

    @staticmethod
    def confirm_work_order(user_id: str, content: str = None) -> List[TextSendMessage]:
        text1 = "請確認工單資訊是否正確" if content is None else content
        text2 = f"以下為工單資訊:\n" \
                f"服務項目: {globals.users[user_id]['service']}\n" \
                f"異常類型: {globals.users[user_id]['anomaly_type']}\n" \
                f"回報時間: {globals.users[user_id]['anomaly_datetime']}\n" \
                f"問題簡述: {globals.users[user_id]['anomaly_brief']}\n" \
                f"狀況詳述: {globals.users[user_id]['anomaly_detail']}"
        yes = globals.confirm_yes
        no = globals.confirm_no
        message = list()
        message.append(TextSendMessage(text=text1))
        message.append(
            TextSendMessage(
                text=text2,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label=yes, text=yes)
                        ),
                        QuickReplyButton(
                            action=MessageAction(label=no, text=no)
                        )
                    ]
                )
            )
        )
        return message

    @staticmethod
    def text_message(content: str) -> TextSendMessage:
        message = TextSendMessage(text=content)
        return message

    @staticmethod
    def image_message(user_id: str) -> ImageSendMessage:
        # original_content_url = f"{globals.server_url}/static/image/{user_id}_{globals.original_image_filename}"
        # preview_image_rul = f"{globals.server_url}/static/image/{user_id}_{globals.preview_image_filename}"
        original_content_url = f"{globals.server_url}/static/image/{user_id}_temp.jpg"
        preview_image_rul = f"{globals.server_url}/static/image/{user_id}_temp.jpg"
        message = ImageSendMessage(original_content_url=original_content_url,
                                   preview_image_url=preview_image_rul)
        return message
