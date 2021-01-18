from test_appium.page_wh.app import App
import pytest

class TestAddMember:

    def setup_class(self):
        self.app = App()

    def teardown_class(self):
        self.app.quit()

    def test_add_member_success(self):
        self.app.start().main().goto_contact().goto_add_member().manual_add_member().add_member('noha','13011100011')


