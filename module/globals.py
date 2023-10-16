service_list = ["異常回報", "新需求提報", "AI助理回應", "新建案提報"]
anomaly_type_list = ["PC、NB、Server硬體問題", "系統問題", "網路異常", "NAS問題", "行政相關", "其它"]
anomaly_modify_list = ["異常類型", "回報時間", "問題簡述", "狀況詳述"]
confirm_yes = "正確"
confirm_no = "修改"
original_image_filename = "original_image_message.jpg"
preview_image_filename = "preview_image_message.jpg"
image_htmlname = "image.html"
server_url = "https://e63e-125-229-3-65.jp.ngrok.io"
users = dict()


def init():
    global service_list
    global anomaly_type_list
    global anomaly_modify_list
    global confirm_yes
    global confirm_no
    global original_image_filename
    global preview_image_filename
    global image_htmlname
    global server_url
    global users
