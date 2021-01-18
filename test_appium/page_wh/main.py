from test_appium.page_wh.base_page import BasePage
from test_appium.page_wh.contact_page import Contact


class Main(BasePage):

    def goto_contact(self):
        '''点击通讯录'''
        self.steps('../page_wh/main.yaml')
        return Contact(self._driver)