# -*- coding: utf-8 -*-
import time
import os
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument('--ignore-certificate-errors')

s = Service('bin/chromedriver')
driver = webdriver.Chrome(service=s, options=options)


# todo 获取access_token
def get_token():
    respon = requests.get(f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={"wxf63dab6abc2027ac"}&secret={"11c7d8db9840bf6f6926cc69b28dd86e"}')
    content = respon.content
    content = content.decode('utf-8')
    data = json.loads(content)
    token = data.get("access_token")
    if token:
        return token
def uniformMessage_send(weapp_template_msg):
    """统一服务消息"""
    token = get_token()
    if not token:
        return False
    url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=" + token
    if weapp_template_msg:
        response = requests.post(url, json=weapp_template_msg)
        content = response.content.decode('utf-8')
        data = json.loads(content)
        print(data)


def sendwxmessage(message):
    ####企业微信消息应用ID
    AgentId = '1000003'
    Secret = 'ysZKeQh_Czx8QO5bFpex8A-zJBm_JLjW0yD4p_d9SlQ'
    CompanyId = 'ww53c0e8c78ee4b0de'
    r = requests.post(
        f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CompanyId}&corpsecret={Secret}').json()
    ACCESS_TOKEN = r["access_token"]
    data = {
        "touser": "@all",
        "msgtype": "text",
        "agentid": f"{AgentId}",
        "text": {"content": f"{message}"}
    }
    data = json.dumps(data)
    r = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={ACCESS_TOKEN}',
                      data=data)

def write_json(data):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "runall.txt")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
    except Exception as e:
        print(f"发生错误：{str(e)}")


if __name__ == '__main__':
    while True:
        try:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(dir_path, "runall.txt")
            print(file_path)
            web_data = json.loads(open(file_path, 'r', encoding='utf_8_sig').read())
            for weblist in web_data[1]["GuoNei"]:
                print(time.asctime(time.localtime(time.time())))
                print('now', weblist["name"], 'pageupdate')
                try:
                    # url = "https://www.fda.gov.tw/tc/news.aspx?cid=3"
                    driver.get(weblist["url"])
                    time.sleep(2)
                    titles = driver.find_element(By.CSS_SELECTOR,weblist["data"])
                    title = titles.text
                    print("newis" +title)
                    print("oldis" + weblist["title"])
                    print('1 cercle have done')
                    driver.quit()
                    # url = titles.get_attribute("href")
                    # print(url)
                    if title != weblist["title"]:
                        weblist["title"] = title
                        print("有更新内容是" + weblist["title"])
                        jsondata = json.dumps(web_data, ensure_ascii=False)  # 序列化简化
                        print('已打包json')
                        write_json(jsondata)
                        print('已写入json文件')
                        # print('发送消息')
                        # urlnotice = "http://wxpusher.zjiecode.com/api/send/message/?appToken=AT_zNMq0y9vMvgbelbxmTqwd7xCYb7mDFJT&content="+ weblist["name"] + weblist["title"] +"&uid=UID_Yfd6ZRU7rWQVCcFYXAus5IfNGQsP&url=http%3a%2f%2fwxpusher.zjiecode.com"
                        # driver.get(urlnotice)
                        print('已发送微信')
                        message = weblist["name"] + "有更新：" + title + "。网址：" + weblist["url"]
                        sendwxmessage(message)
                        print('发送消息')
        
                except FileNotFoundError:
                    print('File not found')
                except json.JSONDecodeError:
                    print('Invalid JSON format')
                except:
                    print('fault')
                    pass
                continue
       

        except:
            print(e)
            print('worong1')
            urlnotice = "http://wxpusher.zjiecode.com/api/send/message/?appToken=AT_zNMq0y9vMvgbelbxmTqwd7xCYb7mDFJT&content=Newfault!&uid=UID_Yfd6ZRU7rWQVCcFYXAus5IfNGQsP&url=http%3a%2f%2fwxpusher.zjiecode.com"
            driver.get(urlnotice)
            print('worongwxmessage')
            driver.quit()
            pass
