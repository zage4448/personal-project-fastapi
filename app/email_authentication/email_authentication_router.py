import os.path
import random
import smtplib

from fastapi import APIRouter
import pickle

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


from pydantic import BaseModel

email_authentication_router = APIRouter()

NAVER_USER_DATA_SAVED_FILE = "email_info/account"


def send_email(smtp_info, naver_user_info, msg):
    with smtplib.SMTP(smtp_info['smtp_server'], smtp_info['smtp_port']) as server:
        server.starttls()

        server.login(naver_user_info['smtp_user_id'], naver_user_info['smtp_user_pw'])

        print(msg.as_string())
        res = server.sendmail(msg["from"], msg["to"], msg.as_string())

        if not res:
            print("이메일 전송 성공!")
        else:
            print(res)


def make_multipart(msg_dict):
    multi = MIMEMultipart(_subtype='mixed')

    for key, value in msg_dict.items():
        if key == 'image':
            with open(value['filename'], 'rb') as fp:
                msg = MIMEImage(fp.read(), _subtype=value['subtype'])

        msg.add_header("Content-Disposition", 'attachment',
                       filename=os.path.basename(value['filename']))

        multi.attach(msg)

    return multi

class RequestEmail(BaseModel):
    email: str

@email_authentication_router.post('/send-email-auth-code')
async def email_notification(request: RequestEmail):
    print("send email to id owner!")

    f = open(NAVER_USER_DATA_SAVED_FILE, 'rb')
    naver_user_info = pickle.load(f)
    f.close()

    smtp_info = dict({
        "smtp_server": "smtp.naver.com",
        "smtp_port": 587
    })

    auth_num_list = []
    for _ in range(6):
        auth_num_list.append(random.randrange(0,10))

    auth_num = ''.join(map(str, auth_num_list))
    auth_message = "인증번호:" + ''.join(map(str, auth_num_list))


    title = '이메일 인증'
    content = auth_message
    sender = naver_user_info['smtp_user_id']
    receiver = request.email

    msg = MIMEText(_text=content, _charset='utf-8')

    multi = MIMEMultipart(_subtype='mixed')

    multi['Subject'] = title
    multi['From'] = sender
    multi['To'] = receiver
    multi.attach(msg)

    send_email(smtp_info, naver_user_info, multi)

    return auth_num