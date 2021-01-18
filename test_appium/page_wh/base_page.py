import yaml
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC


POLL_FREQUENCY = 0.5
TIMEOUT = 30
class BasePage:

    _params = {}  # sendkeys动态传入
    _black_list = [('id', 'image_cancle')]  # 弹窗黑名单
    _error_count = 0  # 初始计数
    _max_count = 10  # 最大计数
    _driver = WebDriver

    def __init__(self, driver: WebDriver = None):
        self._driver = driver

    def quit(self):
        '''退出浏览器'''
        self._driver.quit()

    def refresh(self):
        '''刷新浏览器'''
        self._driver.refresh()

    def get(self, url=''):
        '''打开浏览器'''
        if url != '':
            print('url已传')
            self._driver.get(url)
        else:
            pass

    def find(self, locator):
        '''屏蔽黑名单弹窗封装'''
        try:
            ele = self.find_element(locator)
            self._error_count = 0
            return ele
        except Exception as e:
            self._error_count += 1
            if self._error_count >= self._max_count:
                raise e
            for black in self._black_list:
                eles = self.find_elements(black)
                if len(eles) > 0:
                    eles[0].click()
                    return self.find(locator)
            return e

    def find_element(self, locator):
        '''
        定位一个元素
        :param locator: 传的元素，元祖类型，key定位类型，value元素值
        :return:返回元素对象/False
        '''
        try:
            ele = WebDriverWait(self._driver, timeout=TIMEOUT, poll_frequency=POLL_FREQUENCY). \
                until(EC.presence_of_element_located(locator))
            return ele
        except:
            print('未找到元素》》》》》》》》》》》》》》》》》》，返回None')
            return False

    def find_elements(self, locator):
        '''
        定位一组元素
        :param locator: 传的元素，元祖类型，key定位类型，value元素值
        :return:返回元素对象/None
        '''
        try:
            eles = WebDriverWait(self._driver, timeout=TIMEOUT, poll_frequency=POLL_FREQUENCY).\
                until(lambda x: x.find_elements(*locator))
            return eles
        except:
            print('未找到元素》》》》》》》》》》》》》》》》》》，返回None')
            return False

    def open_yaml(self, path):
        with open(path, encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def steps(self, path='../page/main.yaml'):
        '''封装数据驱动，通过关键字驱动操作'''
        with open(path, encoding='utf-8') as f:
            step_yaml: list[dict] = yaml.load(f, Loader=yaml.FullLoader)
            print(f'yaml数据：{step_yaml}')
            for step in step_yaml:
                if 'by' in step.keys():
                    locator = (step['by'], step['locator'])
                if 'action' in step.keys():
                    if 'click' == step['action']:
                        self.click_new(locator)
                    if 'send' == step['action']:
                        content: str = step['value']
                        for param in self._params:
                            content = content.replace(f'{param}', self._params[param])
                        self.send(locator, content)

    def click_new(self, locator):
        '''输入内容，如果存在弹窗关闭弹窗'''
        try:
            self.find(locator).click()
            self._error_count = 0
        except Exception as e:
            self._error_count += 1
            if self._error_count >= self._max_count:
                raise e
            for black in self._black_list:
                eles = self.find_elements(black)
                if len(eles) > 0:
                    eles[0].click()
                    return self.click_new(locator)
            return e

    def send(self, locator, value):
        '''输入内容，如果存在弹窗关闭弹窗'''
        try:
            self.find(locator).send_keys(value)
            self._error_count = 0
        except Exception as e:
            self._error_count+=1
            if self._error_count >= self._max_count:
                raise e
            for black in self._black_list:
                eles = self.find_elements(black)
                if len(eles) > 0:
                    eles[0].click()
                    return self.send(locator,value)
            return e

    def sendkeys(self, locator, text):
        '''输入内容'''
        try:
            ele = self.find_element(locator)
            ele.send_keys(text)
        except Exception as e:
            print('未找到输入元素')
            raise e

    def clicks(self, locator):
        '''点击元素'''
        try:
            ele = self.find_element(locator)
            ele.click()
        except Exception as e:
            print('未找到点击元素')
            raise e

    def scroll_find_click(self, text):
        '''滑动查找'''
        element = (MobileBy.ANDROID_UIAUTOMATOR,
                   'new UiScrollable(new UiSelector().'
                   'scrollable(true).instance(0)).'
                   'scrollIntoView(new UiSelector().'
                   f'text("{text}").instance(0));')
        self.find_and_click(element)