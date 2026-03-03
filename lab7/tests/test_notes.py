'''
Test
'''

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from lab_7.utils.appium_utils import AppiumDriver

class TestNotes:
    '''
    Test Notes
    '''
    @pytest.fixture(autouse=True, scope="function")
    def _driver(self):
        self.driver = AppiumDriver.get()
        yield
        self.driver.quit()

    def test_add_note(self):
        '''
        Test add note
        '''
        wait = WebDriverWait(self.driver, 10)

        input_field = wait.until(EC.presence_of_element_located(
            (AppiumBy.ID, "com.example.linear.layout.notes:id/note_edit")
        ))
        input_field.send_keys("Zametka")

        add_btn = self.driver.find_element(
            AppiumBy.ID,
            "com.example.linear.layout.notes:id/button_add"
        )
        add_btn.click()

        result = wait.until(
            EC.presence_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().text("Zametka")'
                )
            )
        )
        assert result is not None
