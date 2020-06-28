from selenium import webdriver
import threading
import time
from robot.libraries.BuiltIn import logger

# 套件初始化，只执行一次
def suite_setup():
    pass


# 套件清除，只执行一次
def suite_teardown():
    pass


def broswer_client(username, password):
    try:
        logger.info(f'\n{username}:-- 第 {1} 步 -- {"登陆网站"} \n', True, True)
        wd = webdriver.Chrome()
        # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
        wd.get('http://218.240.148.68:56717/web/index.jsp')
        wd.implicitly_wait(30)
        wd.find_element_by_id('_easyui_textbox_input1').send_keys(username)
        time.sleep(2)
        wd.find_element_by_id('_easyui_textbox_input2').send_keys(password)
        time.sleep(2)
        wd.find_element_by_xpath('//*[@type="button"]').click()
        logger.info(f'\n{username}:-- 第 {2} 步 -- {"遍历访问左边导航菜单"} \n', True, True)
        elements = wd.find_elements_by_xpath("//div[@class='panel-title panel-with-icon']")
        for i,e in enumerate(elements):
            if i == 0:
                continue
            e.click()
            time.sleep(2)

        logger.info(f'\n{username}:-- 第 {3} 步 -- {"遍历访问左边导航菜单"} \n', True, True)
        elements = wd.find_elements_by_xpath("//li/div")
        for i,e in enumerate(elements):
            if i >= 16:
                break
            e.click()
            time.sleep(2)

        logger.info(f'\n{username}:-- 第 {4} 步 -- {"打开一个设备"} \n', True, True)
        element = wd.find_element_by_id("_easyui_tree_2").click()
        time.sleep(2)
        wd.switch_to.frame(wd.find_elements_by_tag_name("iframe")[15])
        time.sleep(2)
        elements = wd.find_elements_by_xpath('''//td[@field="unitId"]/div/a''')
        elements[0].click()

        logger.info(f'\n{username}:-- 第 {5} 步 -- {"10秒钟后关闭浏览器"} \n', True, True)
        time.sleep(10)
        wd.close()
        logger.info(f'\n{username}:-- 第 {6} 步 -- {"测试成功"} \n', True, True)
    except:
        logger.info('---->   !! 不通过!!\n', True, True)
        raise AssertionError(f'\n** 检查点不通过 **  {username} : 访问抛出异常  ')


class c1:
    name = '25个用户同时在线访问'

    # 初始化方法
    def setup(self):
        pass

    # 清除方法
    def teardown(self):
        pass

    def teststeps(self):
        threads = []
        user_pwds =[]
        for i in range(10, 35):
            user_pwds.append(('test' + str(i),'123456'))

        for user_pwd in user_pwds:
            t = threading.Thread(target=broswer_client, args=(user_pwd[0], user_pwd[1]))
            t.setDaemon(True)
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()
