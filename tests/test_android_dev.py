!!! Developer options in Android are hidden settings for debugging and advanced customization, 
enabled by tapping "Build number" seven times under Settings > About phone. !!!!

import os
import unittest
from datetime import datetime

from appium import webdriver
from appium.options.common import AppiumOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ARTIFACT_DIR = "artifacts"

class TestAndroidWeb(unittest.TestCase):
    def setUp(self):

        # Upgrade 3 | Configurable chromedriver
        chromedriver = os.getenv("CHROMEDRIVER_EXECUTABLE")
        if not chromedriver:
            raise RuntimeError(
                "Set CHROMEDRIVER_EXECUTABLE to the full path of a chromedriver binary.\n"
            )

        opts = AppiumOptions()
        opts.set_capability("platformName", "Android")
        opts.set_capability("automationName", "UiAutomator2")
        #opts.set_capability("appium:deviceName", os.getenv("DEVICE_NAME", "Android Emulator"))
        opts.set_capability("appium:deviceName", os.getenv("DEVICE_NAME", "Android Device"))
        #opts.set_capability("deviceName", "Android Emulator")
        opts.set_capability("udid", "48210DLAQ001MV")

        # Optional??
        options.app_package = "com.android.settings"
        options.app_activity = ".Settings"

        # Mobile web in Chrome
        opts.set_capability("browserName", "Chrome")

        # Optional: stability
        opts.set_capability("newCommandTimeout", 120)

        # Upgrade 3 | Explicit but configurable
        opts.set_capability("appium:chromedriverExecutable", chromedriver)

        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)

        # Explicit wait helper (replaces implicit waits)
        self.wait = WebDriverWait(self.driver, 20)
        '''self.driver.implicitly_wait(10)'''

    # Upgrade 4: Screenshot + page source on failure
    def tearDown(self):
        # Detect test failure
        if hasattr(self, "_outcome") and self._outcome.errors:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            os.makedirs(f"{ARTIFACT_DIR}/screenshots", exist_ok=True)
            os.makedirs(f"{ARTIFACT_DIR}/pagesource", exist_ok=True)

            self.driver.save_screenshot(
                f"{ARTIFACT_DIR}/screenshots/failure_{timestamp}.png"
            )

            with open(
                    f"{ARTIFACT_DIR}/pagesource/failure_{timestamp}.html",
                    "w",
                    encoding="utf-8"
            ) as f:
                f.write(self.driver.page_source)
        self.driver.quit()

    '''def test_open_example(self):
        self.driver.get("https://myoppd.com")
        self.assertEqual("MyOPPD Login", self.driver.title)'''

    def test_login_page_has_password_field(self):
        self.driver.get("https://myoppd.com")

        # Upgrade 1 | Explicit wait for a user-visible element on the page
        password_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )

        # Upgrade 2 | User-visible assertion (stronger than checking <title>)
        self.assertTrue(password_input.is_displayed(), "Password field should be visible on the login page")

if __name__ == "__main__":
    unittest.main()
