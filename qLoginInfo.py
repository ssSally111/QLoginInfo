import os
import re
import sys
import time
import execjs
import requests
from random import *
from retrying import retry


# tx hash33加密算法
def hash33(t33):
    e = 0
    for i in range(len(t33)):
        e += (e << 5) + ord(t33[i])
    return 2147483647 & e


# 获取cookie
def login():
    ss = requests.session()
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=' + str(
        '0.' + str(int(random() * 10000000000000000)))
    response = ss.get(url=url)
    with open('qrcode.png', 'wb') as f:
        f.write(response.content)
    os.system("start explorer " + ScriptPath + "\\qrcode.png")
    # os.system("start explorer " + ScriptPath + "\\Duks.exe")
    cookie = response.cookies
    headers = requests.utils.dict_from_cookiejar(cookie)
    while True:
        url = f'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.Html' \
              f'%3Fpara%3Dizone%26from%3Diqq&ptqr' \
              f'token={hash33(headers["qrsig"])}&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0' \
              f'-1542784335061&js_ver=10289&js_type=1&login_sig=hn6ZiMZRPT8LWFsFG3MrScznzLVrdbwS9EIo-ihAmeD' \
              f'*YmOfqP3uoI6JytVVQYw2&pt_uistyle=40&aid=549000912&daid=5& '
        html = ss.get(url=url, headers=headers)
        html.encoding = 'utf-8'
        typei = re.findall('[\u4e00-\u9fa5]+', html.text)[0]
        if typei == '二维码未失效':
            full_path = DIRECTORY + '\\log.txt'
            file = open(full_path, 'w')
            file.write(typei)
            file.close()
        elif typei == '二维码认证中':
            full_path = DIRECTORY + '\\log.txt'
            file = open(full_path, 'w')
            file.write(typei)
            file.close()
        elif typei == '登录成功':
            full_path = DIRECTORY + '\\log.txt'
            file = open(full_path, 'w')
            file.write(typei)
            file.close()
            pt_recent_uins = re.findall(r"<Cookie pt_recent_uins=(.+?) for .p", str(html.cookies))[0]
            pt2gguin = re.findall(r"<Cookie pt2gguin=(.+?) for .p", str(html.cookies))[0]
            uin = re.findall(r"<Cookie uin=(.+?) for .q", str(html.cookies))[0]
            ptnick_qq = re.findall(r"=(.+?) for .q", str(html.cookies))[3]
            skey = re.findall(r"<Cookie skey=(.+?) for .q", str(html.cookies))[0]
            superkey = re.findall(r"<Cookie superkey=(.+?) for .p", str(html.cookies))[0]
            supertoken = re.findall(r"<Cookie supertoken=(.+?) for .p", str(html.cookies))[0]
            superuin = re.findall(r"<Cookie superuin=(.+?) for .p", str(html.cookies))[0]
            RK = re.findall(r"<Cookie RK=(.+?) for .q", str(html.cookies))[0]
            ptcz = re.findall(r"<Cookie ptcz=(.+?) for .q", str(html.cookies))[0]
            headers_2 = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50',
                'Referer': 'https://xui.ptlogin2.qq.com/',

                # Cookie这里空参数的给删了,需要自己加(之前写完的代码找不到了)
                'Cookie': 'pgv_pvi=; pgv_pvid=; RK=; '
                          'ptcz=; '
                          'eas_sid=; tvfe_boss_uuid=; '
                          'LW_uid=; iip=; _ga=; '
                          'ied_qq=; uin_cookie=; sd_userid=; '
                          'sd_cookie_crttime=; o_cookie=; '
                          '_tc_unionid=; QZ_FE_WEBP_SUPPORT=; '
                          'pac_uid=; LW_sid=; luin=; '
                          'lskey'
                          '=; '
                          '__Q_w_s__QZN_TodoMsgCnt=; ptui_loginuin=; Loading=Yes; qqmusic_uin=; '
                          'qqmusic_key=; qqmusic_fromtag=; _qpsvr_localtk=; '
                          'pgv_info=ssid=; qzmusicplayer=; '
                          'cpu_performance_v8=;'
                          ''
                          ' _qz_referrer=i.qq.com; uin=' + uin + '; skey=' + skey
            }
            url_2 = re.sub('(c.html%3Fpara)', r'\1%3Dizone',
                           str(re.findall(r"'0','0','(.+?)','0", str(html.content))[0])).replace('%26from%3Diqq',
                                                                                                 '').replace(
                'ucc.Html%3', 'ucc.html%3')
            html_2 = requests.get(url_2, headers_2)
            cookie_2 = dict(html_2.request.headers)['Cookie']
            p_uin = re.findall(r"p_uin=(.+?); ", cookie_2)[0]
            pt4_token = re.findall(r"pt4_token=(.+?); ", cookie_2)[0]
            p_skey = re.findall(r"p_skey=(.+?)_", cookie_2)[0] + '_'
            cookie_3 = {
                'uin': uin,
                'p_uin': p_uin,
                'superuin': superuin,
                'skey': skey,
                'p_skey': p_skey,
                'superkey': superkey,
                'pt4_token': pt4_token,
                'supertoken': supertoken,
                'pt2gguin': pt2gguin,
                'pt_recent_uins': pt_recent_uins,
                'ptnick_qq': ptnick_qq,
                'ptcz': ptcz,
                'RK': RK
            }
            return cookie_3
        else:
            # print("二维码已失效，请重新扫码！")
            full_path = DIRECTORY + '\\log.txt'
            file = open(full_path, 'w')
            file.write(typei)
            file.close()
            login()
        time.sleep(2)


# get请求
@retry(stop_max_attempt_number=3)
def _get(url, headers):
    response = requests.get(url=url, headers=headers, timeout=10)
    return response.content.decode()


def get(url, headers):
    try:
        html_str = _get(url, headers)
    except:
        html_str = None
    return html_str


# tx pgv加密算法
def pgv_():
    pgv_pvi = execjs.compile(open(r"pgv_.js").read().encode('utf-8').decode('unicode_escape')).call('pgv_pvi_', '')
    pgv_si = execjs.compile(open(r"pgv_.js").read().encode('utf-8').decode('unicode_escape')).call('pgv_si_', '')
    pgv_pvid = execjs.compile(open(r"pgv_.js").read().encode('utf-8').decode('unicode_escape')).call('pgv_pvid_', '')
    pgv_info_ssid = execjs.compile(open(r"pgv_.js").read().encode('utf-8').decode('unicode_escape')).call(
        'pgv_info_ssid_', '')
    pgv_dick = {
        'pgv_pvi': pgv_pvi,
        'pgv_si': pgv_si,
        'pgv_pvid': pgv_pvid,
        'pgv_info_ssid': pgv_info_ssid
    }
    return pgv_dick


'''







'''

# 程序主入口
if __name__ == '__main__':
    # 初始化
    # 获取运行路径
    DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    ScriptPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
    cookie = login()
    pgv_x = pgv_()

    # 数据
    # ******************************************
    qq = str(cookie['uin']).replace('o', '')
    nick = ''
    uid = str(cookie['uin'])
    skey = str(cookie['skey']).replace('@', '')
    bkn = str(execjs.compile(open(r"pgv_.js").read().encode('utf-8').decode('unicode_escape')).call('t', 'Z' + skey))
    p_skey = str(cookie['p_skey'])
    pt4_token = str(cookie['pt4_token'])
    superkey = str(cookie['superkey'])
    supertoken = str(cookie['supertoken'])
    ptcz = str(cookie['ptcz'])
    RK = str(cookie['RK'])
    pt_recent_uins = str(cookie['pt_recent_uins'])
    pt2gguin = str(cookie['pt2gguin'])
    pgv_pvi = str(pgv_x['pgv_pvi'])
    pgv_si = str(pgv_x['pgv_si'])
    pgv_pvid = str(pgv_x['pgv_pvid'])
    pgv_info_ssid = str(pgv_x['pgv_info_ssid'])
    # ******************************************
    full_path = DIRECTORY + '\\logs.ini'
    file = open(full_path, 'w')
    file.write(qq)
    file.close()

    # 请求

    # 访客


    # 运动




    # 游戏


    # 打卡






    # 管家

    # 等待30分
    time.sleep(1801)

    # 管家领取

    file = open(full_path, 'a')
    file.write('管家加速ok')
    file.close()
