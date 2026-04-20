import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
import datetime as dt
import json
import tkinter as tk
import argparse
import logging



class SelectDialog:
    def __init__(self,root,class_list):
        self.root = root
        self.info_label = tk.Label(root, text="请选择想要刷进度的课程")
        self.info_label.pack(pady=5)
        self.submit_button = tk.Button(root, text="选择", command=self.get_text)

        self.lb = tk.Listbox(self.root, height=len(class_list), width=50)
        for class_name in class_list:
            self.lb.insert(tk.END, class_name)
        self.lb.pack(pady=5)
        self.submit_button.pack(pady=5)
        self.class_data = ""
    def get_text(self):
        self.class_data = self.lb.get(self.lb.curselection())
        self.root.destroy()



def fun1(driver,text):
    if len(text)>1000:
        text = text[:1000]
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[2]/div[2]/a').click()
    time.sleep(3)
    dialog = driver.find_element(By.CSS_SELECTOR, '#comment-create-textarea')
    dialog.send_keys(text)
    submit_btn = driver.find_element(By.CSS_SELECTOR, '#text-wrapper > div.btn-group.text-right > a')
    submit_btn.click()


def manual_login(driver):
    try:
        driver.get('https://bjpc.cep.webtrn.cn/np/#/login')
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            un = config["un"]
            pw = config["pw"]
        print("已加载配置文件！")
    except FileNotFoundError:
        print("未找到配置文件，请输入：")
        un = input("请输入你的学号：\n")
        pw = input("请输入密码:\n")
        token = 0
        hint = 0
        if hint == "0":
            hint = "尽可能接地气，不要使用Markdown格式输出"
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump({"un": un, "pw": pw, "token": token, "hint": hint}, f)

    try:
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                 "iframe[src='https://bjpc-ucenter.webtrn.cn/center/login?self_redirect=false&redirect_uri=https://bjpc.cep.webtrn.cn/np']")
                                                                                ))
    except exceptions.TimeoutException as e:
        logging.error("发生了一个错误:%s",e)
        exit(1)
    driver.switch_to.frame(iframe)
    username = driver.find_element(By.CSS_SELECTOR, "input[placeholder='请输入用户名']")
    username.send_keys(un)
    password = driver.find_element(By.CSS_SELECTOR, "input[placeholder='请输入密码']")
    password.send_keys(pw)
    driver.find_element(By.CSS_SELECTOR, "#up-login-btn").click()

#配置无头模式
def main():
    logging.basicConfig(level=logging.ERROR,filename='error.log',filemode='a',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--driver_path', type=str, default="chromedriver\\chromedriver.exe",
                        help='chromedriver路径')
    parser.add_argument('-b', '--binary_path', type=str, default="chrome\\chrome.exe",
                        help='chrome或chrome-headless-shell路径')
    parser.add_argument('-n', '--no_headless', action='store_true', default=False, help="禁用headless模式")
    parser.add_argument('-l', '--legacy', action='store_true', default=False,
                        help='旧版账号密码登录选项，默认为0:用户企业微信扫描二维码登录，可选1:使用已保存的账号密码登录')
    args = parser.parse_args()

    driver_path = args.driver_path
    binary_path = args.binary_path
    no_headless = args.no_headless
    legacy_login = args.legacy
    options = webdriver.ChromeOptions()
    options.binary_location = binary_path
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--mute-audio")
    if not no_headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        # driver.execute_script("window.location.href = 'https://bjpc.cep.webtrn.cn/npapi/open/casLogin/login';")
        print('已开启无头模式')
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service,options=options)
    driver.set_window_size(1920, 1080)
    print("框架初始化完毕!")
    # --------登录教学平台--------

    if legacy_login:
        manual_login(driver)
    else:
        try:
            driver.get('https://bjpc.cep.webtrn.cn/npapi/open/casLogin/login')
        except TimeoutError:
            print("加载超时，请检查网络连接！")
        driver.save_screenshot('temp.png')
        try:
            print("请使用企业微信扫码登录后关闭弹窗")
            import matplotlib.pyplot as plt
            import matplotlib.image as mpimg
            # 显示二维码
            image = mpimg.imread('temp.png')
            plt.imshow(image)
            plt.show()
        except KeyboardInterrupt:
            os.remove('temp.png')
            driver.quit()
            exit(1)
        try:
            WebDriverWait(driver, 30).until(EC.url_matches('https://bjpc.cep.webtrn.cn/ws/#/ws/ws/student/index/right'))
            os.remove('temp.png')
        except exceptions.TimeoutException as e:
            logging.error("发生了一个错误:%s", e)
            driver.quit()
            exit(1)
        except TimeoutError:
            logging.error("加载超时")
            print("加载超时，请检查网络连接！")
            driver.quit()
            exit(1)

    print("登录成功!")
    # 选择课程
    driver.switch_to.default_content()
    try:
        frame = WebDriverWait(driver, 10, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#popup-mytodostudy')))
        driver.execute_script("arguments[0].style = 'display: none;';", frame)
    except exceptions.TimeoutException:
        print("未检测到待办事项")
    driver.switch_to.default_content()
    iframe = WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='mainRight']")))
    driver.switch_to.frame(iframe)

    # test = driver.find_element(By.CSS_SELECTOR,'#cosTab2')
    # test.click()
    # time.sleep(2)

    all_cells = WebDriverWait(driver, 10, 1).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "cell"))
    )


    c_list=[]
    # 遍历每个课程卡片
    for cell in all_cells:
        try:
            # 3. 在当前卡片内查找课程标题
            # 标题在 <div class="title"> 标签内
            title_element = cell.find_element(By.CLASS_NAME, "title")
            c_list.append(title_element.text)
        except exceptions:
            # 如果某个卡片结构异常，跳过继续查找下一个
            continue
    a = tk.Tk()
    a.title("选择")
    select_app = SelectDialog(a,c_list)
    a.mainloop()
    target_course_name = select_app.class_data
    if target_course_name == "":
        driver.quit()
        exit(1)
    try:
        for cell in all_cells:
            title_element = cell.find_element(By.CLASS_NAME, "title")
            if title_element.text.strip() == target_course_name:
                start_button = cell.find_element(By.CSS_SELECTOR, "a.btn.btn-solid-primary")
                link = start_button.get_attribute("href")
                driver.execute_script(f"window.open('{link}')")
                print(f"已跳转到课程'{target_course_name}'的界面。")
    except exceptions as e:
        print(f"出现异常错误:{e}")
        logging.error("跳转课程界面中出现问题：%s", e)
        driver.quit()
        exit(1)

    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    start_time = dt.datetime.now()
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[@id='learnHelperIframe']")))
        driver.switch_to.frame(iframe)
    except exceptions.TimeoutException as e:
        print("加载课程信息时出现问题，请检查课程是否可用")
        logging.error("加载课程信息中出现问题：%s", e)
        driver.quit()
        exit(1)
    driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[1]/a').click()
    driver.switch_to.default_content()
    iframe = driver.find_element(By.XPATH, "//iframe[@id='mainContent']")
    driver.switch_to.frame(iframe)
    chapters = driver.find_elements(By.CSS_SELECTOR, ".s_sectionlist")
    for chapter in chapters:
        driver.execute_script("arguments[0].style = 'display: block;';", chapter)
    sections = driver.find_elements(By.CSS_SELECTOR, ".s_sectionwrap")
    for section in sections:
        driver.execute_script("arguments[0].style = '';", section)
    print("加载完成！")
    chapters = driver.find_elements(By.XPATH, "//*[@completestate='0']")
    for index, chapter in enumerate(chapters):
        time.sleep(3)
        flag = chapter.get_attribute("itemtype")
        ActionChains(driver).move_to_element(chapter).click(chapter).perform()
        os.system('cls')
        title = chapter.get_attribute("title")
        print(
            f"名称：{title}\n类型：{flag}\n进度：{index+1}/{len(chapters)} ({(index / len(chapters) * 100):.2f}%)")
        if flag == 'video':
            try:
                iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//iframe[@id='mainFrame']")))
                driver.switch_to.frame(iframe)
                time.sleep(10)
                bar = driver.find_element(By.CSS_SELECTOR, "#screen_player")
                driver.execute_script("arguments[0].style = 'display: block;';", bar)
                btn = driver.find_element(By.CSS_SELECTOR, "#player_pause_btn > a")
                b_str = driver.find_element(By.CSS_SELECTOR, "#player_pause_btn > a > i").get_attribute("class")
                time.sleep(3)
                driver.execute_script("arguments[0].style = 'display: block;';", bar)
                if b_str == "coursespace screen-player-btn-icon icon-play-sp-fill":
                    btn.click()
                speed = driver.find_element(By.CSS_SELECTOR, '#li_speedval_cur')
                driver.execute_script("arguments[0].style = 'display: block;';", bar)
                ActionChains(driver).move_to_element(speed).perform()
                speed_x = driver.find_element(By.CSS_SELECTOR, '#li_speed > ul > li:nth-child(1) > a')
                driver.execute_script("arguments[0].style = 'display: block;';", bar)
                ActionChains(driver).move_to_element(speed_x).click(speed_x).perform()
            except Exception as e:
                logging.error("初始化视频中出现问题：%s", e)
                driver.save_screenshot("error.png")
                driver.quit()
                exit(1)
            try:
                kill_count = 0
                time1 = WebDriverWait(driver, 10, 0.5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#screen_player_time_1'))).text
                time2 = driver.find_element(By.CSS_SELECTOR, '#screen_player_time_2').text
                time2_conv = dt.datetime.strptime(time2, "%M:%S")
                while True:
                    time1= driver.find_element(By.CSS_SELECTOR, '#screen_player_time_1').text
                    while time1 == '':
                        driver.execute_script("arguments[0].style = 'display: block;';", bar)
                        time1 = driver.find_element(By.CSS_SELECTOR, '#screen_player_time_1').text
                    time_conv = dt.datetime.strptime(time1, "%M:%S")

                    time_rt = dt.datetime.now()
                    # if time_conv.second % 30 == 0:
                    #     print(f"{time1}/{time2}")
                    os.system('cls')
                    print(
                        f"名称：{title}\n类型：{flag}\n进度：{index + 1}/{len(chapters)} ({(index / len(chapters) * 100):.2f}%)")

                    print(f"{((time_conv.minute*60+time_conv.second) * 100 / (time2_conv.minute*60+time2_conv.second)):.2f}%")
                    time.sleep(1)
                    time1_new = driver.find_element(By.CSS_SELECTOR, '#screen_player_time_1').text

                    if time1_new == time1:
                        if kill_count>5:
                            exit(2)
                        driver.execute_script("arguments[0].style = 'display: block;';", bar)
                        btn.click()
                        time.sleep(1)
                        btn.click()
                        kill_count += 1
                    else:
                        kill_count -= 1
                    if time1 == time2 and (time1 != '' or time2 != ''):
                        break
                    if (time_rt - start_time).total_seconds() > 1800:
                        driver.switch_to.default_content()
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".layui-layer-btn0"))).click()
                        start_time = dt.datetime.now()
                        driver.switch_to.frame(iframe)
                driver.switch_to.default_content()
                iframe = driver.find_element(By.XPATH, "//iframe[@id='mainContent']")
                driver.switch_to.frame(iframe)
            except exceptions.NoSuchElementException as e:
                logging.error("播放视频中出现问题：%s",e)
                driver.save_screenshot("error.png")
                driver.quit()
                exit(1)
            except exceptions.TimeoutException as e:
                logging.error("网络错误：%s",e)
        elif flag == 'doc' or flag == 'resource' or flag == 'link':
            time.sleep(5)
        elif flag == 'topic':
            driver.switch_to.default_content()
            iframe = driver.find_element(By.XPATH, "//iframe[@id='mainContent']")
            driver.switch_to.frame(iframe)
            cid = driver.find_element(By.CSS_SELECTOR, '#prev_item_id').get_attribute("value")
            iframe = driver.find_element(By.XPATH, "//iframe[@id='mainFrame']")
            driver.switch_to.frame(iframe)
            iframe = driver.find_element(By.XPATH, f"//iframe[@id='discuss-container-{cid}']")
            driver.switch_to.frame(iframe)
            title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                    "#app > div > div.space-row.space-comment-topic.sharp.shadow-light.webWidth-md > div.space-row-head.edge > span.title"))).text
            try:
                desc = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[1]/p/p').text
            except exceptions.NoSuchElementException:
                desc = ""
            print(f"问题：{title},{desc}")
            try:
                driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[2]/div[2]/a')
            except exceptions.NoSuchElementException:
                print("讨论已无法参与！")
                driver.switch_to.default_content()
                iframe = driver.find_element(By.XPATH, "//iframe[@id='mainContent']")
                driver.switch_to.frame(iframe)
                continue
            driver.switch_to.default_content()
            iframe = driver.find_element(By.XPATH, "//iframe[@id='mainContent']")
            driver.switch_to.frame(iframe)
            continue
        else:
            print("此内容过于敏感，请手动完成！")
            continue

    print("所有内容已全部刷完！！")
    mode=input("是否进入挂机模式?[y]/n")
    if mode == 'n':
        driver.quit()
        exit(1)
    else:
        try:
            driver.switch_to.default_content()
            while True:
                btn = WebDriverWait(driver,1830,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.layui-layer-btn0')))
                btn.click()
        except KeyboardInterrupt:
            tme = driver.find_element(By.ID, "learnTimer")
            print(tme.text)
            driver.quit()
            os.system("pause")
            exit(1)


if __name__ == "__main__":
    main()
