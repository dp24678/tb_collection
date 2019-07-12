import asyncio
import json
import random
import base64
import re
import time
from pyppeteer import launch
import requests
from config import ACCOUNT_PASSWORD,js1,js2,js3,js4



async def taobao_login():
    """
    淘宝登录主程序
    :param username: 用户名
    :param password: 密码
    :param url: 登录网址
    :return: 登录cookies
    """
    # 'headless': False如果想要浏览器隐藏更改False为True
    browser = await launch({'headless': False , 'args': [
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            "--window-size=1500,900",
        ]})

    page = await browser.newPage()
    await page.setViewport({"width": 1920, "height": 1080})

    await page.setExtraHTTPHeaders({
        'Proxy-Authorization': make_proxy_authorization()
    })

    await page.evaluateOnNewDocument('''() = > {
        const originalQuery = window.navigator.permissions.query;
        return window.navigator.permissions.query = (parameters) = > (
                parameters.name === 'notifications' ?
                Promise.resolve({state: Notification.permission}):
                originalQuery(parameters)
                );
        }''')
    await page.goto('https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F')

    await set_js(page)

    return page ,browser


async def set_js(page):
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
    await page.evaluate(js1)
    await page.evaluate(js2)
    await page.evaluate(js3)
    await page.evaluate(js4)


async def password_login(page, username, password):
    # 输入用户名，密码
    try:
        await page.click('#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
    except:
        pass
    await page.waitFor('#TPL_username_1')
    await page.type('#TPL_username_1', username, {'delay': 200})  # delay是限制输入的时间
    time.sleep(random.uniform(1, 1.5))
    await page.type('#TPL_password_1', password,{'delay': 250})
    time.sleep(random.uniform(0, 1))
    # 检测页面是否有滑块。原理是检测页面元素。
    slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块
    if slider:
        print('当前页面出现滑块')
        flag = await mouse_slide(page)  # js拉动滑块过去。
        return flag
    return True


# 获取登录后cookie
async def get_cookie(username, password):
    global status_login
    page,browser = await taobao_login()
    for i in range(3):
        status_login = await password_login(page, username, password)
        if status_login:
            break
        print('尝试重新获取----------')
        await page.reload()
    if not status_login:
        return False

    await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')  # 如果无法通过回车键完成点击，就调用js模拟点击登录按钮。
    await page.waitFor(2000)
    # await page.waitForNavigation()
    title=await page.title()
    print(title,type(title))
    if '登录' in title:
        print('出现手机验证码')
        st = await input_code(page,username)  # 检测到需要输入手机验证码，获取并输入
        if st is None:  # 如果一直获取不到验证码，就直接跳过
            return
        else:
            pass
    try:
        await page.waitFor('.site-nav-user')
    except:
        return False
    cookies_list = await page.cookies()

    cookies = {}
    for cookie in cookies_list:
        cookies[cookie.get('name')]=cookie.get('value')

    await page.close()
    await browser.close()
    return json.dumps(cookies)


async def mouse_slide(page):

    await asyncio.sleep(1)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1_n1z')  # 不同场景的验证码模块能名字不同。
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return False
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        if slider_again != '验证通过':
            return False
        return True


async def get_queryid_from_username(username):
    """
    获取用户名对应的查询码
    :param username:用户名
    :return: 查询码
    """
    for el in ACCOUNT_PASSWORD:
        if el[0] == username:
            return el[2]


async def input_code(page,username):
    global yzm
    frame_list=page.frames
    fra=frame_list[1]
    await fra.waitFor('.ui-form-item')
    time.sleep(2)
    await fra.click("div.checkcode-warp > #J_GetCode")
    for i in range(5):
        yzm=await get_code(await get_queryid_from_username(username))
        if not yzm:  # 如果验证码一直获取不到 重新发送验证码
            await fra.click("div.checkcode-warp > #J_GetCode")
        else:
            await fra.type("#J_Phone_Checkcode", yzm, {'delay': 150})
            print('输入验证码====开始点击确定')
            time.sleep(2)
            await fra.click('#submitBtn')
            break

    return yzm


async def get_code(queryid):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    FormData = {'queryID':queryid }
    time.sleep(3)
    for i in range(15):
       print('-----获取验证码-----')
       response = requests.post('http://47.98.182.150/yzm/', data=FormData, headers=headers)
       # with open('aa.html', 'wb') as f:
       #     f.write(response.content)
       yzm_ = re.findall(r"#4169E1'>(\d*?)</span>", response.text)
       print('验证码：',yzm_)
       if len(yzm_) > 0:
          return yzm_[0]
       time.sleep(2)


def getCookie(username,password):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(get_cookie(username, password))
    loop.run_until_complete(task)
    cookie = task.result()
    return cookie


def make_proxy_authorization():
    proxyUser = 'H0026G1TP41J843D'
    proxyPass = '*****'
    proxy_authorization = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
    return proxy_authorization





