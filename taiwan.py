
from http.client import ImproperConnectionState
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By


# 配置选项
options = webdriver.ChromeOptions()
# 忽略证书错误
options.add_argument('--ignore-certificate-errors')
# 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 忽略 DevTools listening on ws://127.0.0.1... 提示
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# 获取驱动
driver = webdriver.Chrome(options=options)


# todo 获取access_token
def get_token():
    respon = requests.get(
        f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={"wxf63dab6abc2027ac"}&secret={"11c7d8db9840bf6f6926cc69b28dd86e"}')
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
    f = open('taiwan.txt', 'w')
    f.write(data)
    f.close()


if __name__ == '__main__':
    try:
        web_data = json.loads(open('taiwan.txt', 'r',encoding="utf-8").read())
                  

        # time.sleep(20)
        for weblist in web_data[1]["GuoNei"][0:1]:
            print(time.asctime(time.localtime(time.time())))
            print('now', weblist["name"], 'pageupdate')
            try:
                # browser.get(weblist["url"])
                driver.get("https://www.fda.gov.tw/tc/news.aspx?cid=3")
                time.sleep(2)
                titles = driver.find_element(By.CSS_SELECTOR, "#mp-pusher > div > div.mainContentWrap.withLeft > table > tbody > tr:nth-child(1) > td:nth-child(2) > a")

                title = titles.text
                print("newis是" +title)
                print("oldis是" + weblist["title"])
                # url = titles.get_attribute("href")
                # print(url)
                if title == weblist["title"]:
                    weblist["title"] = title
                    print("有更新内容是" + weblist["title"])
                    jsondata = json.dumps(web_data, ensure_ascii=False)  # 序列化简化
                    print('已打包json')
                    write_json(jsondata)
                    print('已写入json文件')
                    print('发送消息')
                    urlnotice = "http://wxpusher.zjiecode.com/api/send/message/?appToken=AT_zNMq0y9vMvgbelbxmTqwd7xCYb7mDFJT&content="+ weblist["name"] + weblist["title"] +"&uid=UID_Yfd6ZRU7rWQVCcFYXAus5IfNGQsP&url=http%3a%2f%2fwxpusher.zjiecode.com"
                    driver.get(urlnotice)
                    print('已发送微信')
                    # message = weblist["name"] + "有更新：" + title + "。网址：" + url
                    # sendwxmessage(message)
                    # print('发送消息')
                    # if "全国未准入境" in title:
                    #
                    #     browser.get(url)
                    #
                    #     content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#easysiteText > p:nth-child(1)"))).text
                    #     print(content)
                    #     link1 = ''
                    #     link2 = ''
                    #     try:
                    #         link1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#easysiteText > p:nth-child(2) > a"))).get_attribute("href")
                    #     except:
                    #         print('检索', weblist["name"], '未找到链接1')
                    #         link1 = ''
                    #
                    #     try:
                    #         link2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#easysiteText > p:nth-child(3) > a"))).get_attribute("href")
                    #     except:
                    #         print('检索', weblist["name"], '未找到链接2')
                    #         link2 = ''
                    #
                    #     print(link1)
                    #     print(link2)
                    #     locale.setlocale(locale.LC_ALL, 'en')
                    #     locale.setlocale(locale.LC_CTYPE, 'chinese')
                    #     datecontent = datetime.now().strftime('%Y年%m月%d日')
                    #     foodsafecontent = "    " + datecontent + "，海关总署发布" + title +"，"+ content+  "具体信息结果可查询附件链接：" + link1 +";"+ link2
                    #     print(foodsafecontent)
                    #     foodsafetitle = "海关总署发布" + title
                    #     foodsafepublishOrg = "海关总署"
                    #     foodsafeurl = url
                    #     foodsafdate = datetime.now().strftime('%Y-%m-%d')
                    #     postfoodsafemassage(foodsafetitle, foodsafepublishOrg, foodsafeurl, foodsafdate, foodsafecontent)
                    #     # sendwxmessage(foodsafecontent)
                    #     print('发送消息')
                    #     urlnotice = "http://wxpusher.zjiecode.com/api/send/message/?appToken=AT_zNMq0y9vMvgbelbxmTqwd7xCYb7mDFJT&content=New!&uid=UID_Yfd6ZRU7rWQVCcFYXAus5IfNGQsP&url=http%3a%2f%2fwxpusher.zjiecode.com"
                    #     browser.get(urlnotice)
                    #     print('已发送微信')


            except:
                print('检索', weblist["name"], 'fault')
                pass
            continue

        # browser.close()
        # browser.quit()
        print('检索完成，等待60秒下一轮')
        # try:
        #     print('-----清除缓存-----------')
        #     browser.get('chrome://settings/clearBrowserData')
        #     time.sleep(2)
        #     clearButton = browser.execute_script(
        #         "return document.querySelector('settings-ui').shadowRoot.querySelector('settings-main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('settings-section > settings-privacy-page').shadowRoot.querySelector('settings-clear-browsing-data-dialog').shadowRoot.querySelector('#clearBrowsingDataDialog').querySelector('#clearBrowsingDataConfirm')")
        #     clearButton.click()
        #     print('-----清除缓存完成-----------')
        #     time.sleep(10)
        # except:
        #     pass
    except:
        # print(e)
        print('检新失败')
        urlnotice = "http://wxpusher.zjiecode.com/api/send/message/?appToken=AT_zNMq0y9vMvgbelbxmTqwd7xCYb7mDFJT&content=Newfault!&uid=UID_Yfd6ZRU7rWQVCcFYXAus5IfNGQsP&url=http%3a%2f%2fwxpusher.zjiecode.com"
        driver.get(urlnotice)
        print('已发送微信')
        pass



# driver.get("https://www.baidu.com")

# driver.find_element(By.ID, "kw").send_keys("测试蔡坨坨")
# driver.find_element(By.ID, "su").click()
# time.sleep(3)

# driver.quit()

