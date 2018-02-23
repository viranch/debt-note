from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Driver(object):
    def __init__(self):
        opts = Options()
        opts.add_argument("--headless")
        self._d = webdriver.Chrome(chrome_options=opts)

    def wait_for(self, selector, by=By.XPATH, timeout=9999):
        return WebDriverWait(self._d, timeout).until(EC.visibility_of_element_located((by, selector)))

    def wait_for_invisibility(self, selector, by=By.XPATH):
        return WebDriverWait(self._d, 9999).until(EC.invisibility_of_element_located((by, selector)))

    def click(self, selector, by=By.XPATH, timeout=9999):
        try:
            return self.wait_for(selector, by, timeout).click()
        except TimeoutException:
            return None

    def type_input(self, value, selector, by=By.NAME):
        elem = self.wait_for(selector, by)
        elem.clear()
        elem.send_keys(value)

    def __getattr__(self, name):
        return getattr(self._d, name)
