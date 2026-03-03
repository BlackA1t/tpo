'''
Utils
'''

from appium import webdriver
from appium.options.android import UiAutomator2Options

class AppiumDriver:
    '''
    Appium Driver
    '''
    @staticmethod
    def get(
        app=r"D:\Code\vscode\test\lab_7\app\apk\notes.apk",
        device_name="emulator-5554"
    ):
        '''
        Get Appium Driver
        '''
        options = UiAutomator2Options().load_capabilities({
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "udid": device_name,
            "deviceName": device_name,
            "app": app,
            "noReset": True,
            "newCommandTimeout": 120
        })

        return webdriver.Remote(
            "http://localhost:4723", 
            options=options
        )
