import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Driver(object):
    def __enter__(self):
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--window-size=1920x1080")
        self._d = webdriver.Chrome(chrome_options=opts)
        return self

    def wait_for(self, selector, by=By.XPATH, timeout=15):
        return WebDriverWait(self._d, timeout).until(EC.visibility_of_element_located((by, selector)))

    def wait_for_invisibility(self, selector, by=By.XPATH):
        return WebDriverWait(self._d, 15).until(EC.invisibility_of_element_located((by, selector)))

    def click(self, selector, by=By.XPATH, timeout=15):
        try:
            return self.wait_for(selector, by, timeout).click()
        except TimeoutException:
            return None

    def type_input(self, value, selector, by=By.NAME):
        elem = self.wait_for(selector, by)
        elem.clear()
        elem.send_keys(value)

    def load_cookies(self, module):
        filename = '{}_cookies.pkl'.format(module)
        try:
            cookies = pickle.load(open(filename, 'rb'))
            for cookie in cookies:
                self._d.add_cookie(cookie)
        except IOError:
            pass

    def dump_cookies(self, module):
        filename = '{}_cookies.pkl'.format(module)
        pickle.dump(self._d.get_cookies() , open(filename, 'wb'))

    def __getattr__(self, name):
        return getattr(self._d, name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._d.quit()
