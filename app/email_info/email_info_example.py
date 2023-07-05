import pickle


NAVER_USER_DATA_SAVED_FILE = 'app/email_info/account'

naver_user_info = dict({
    'smtp_user_id': '이메일',
    'smtp_user_pw': '비밀번호',
})

f = open(NAVER_USER_DATA_SAVED_FILE, 'wb')
pickle.dump(naver_user_info, f)
f.close()