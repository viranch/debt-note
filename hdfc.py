from selenium.webdriver.common.by import By
from driver import Driver

class HDFC(object):
    def __init__(self):
        self.driver = Driver()

    def get_unbilled(self, username, password):
        # login
        print 'Logging in'
        self.driver.get('https://netbanking.hdfcbank.com/netbanking/')
        self.driver.switch_to.frame('login_page')
        self.driver.type_input(username, 'fldLoginUserId')
        self.driver.click('//img[@alt="continue"]')
        self.driver.type_input(password, 'fldPassword')
        self.driver.click('chkrsastu', by=By.NAME)
        self.driver.click('//img[@alt="Login"]')

        # read unbilled message
        print 'Reading data'
        self.driver.switch_to.frame('main_part')
        unbilled = self.driver.wait_for('CCActiveMatSummary1', By.ID).text
        self.driver.switch_to.default_content()

        # logout
        print 'Logging out'
        self.driver.switch_to.frame('common_menu1')
        self.driver.click('//img[@alt="Log Out"]')

        # quit
        self.driver.quit()

        return unbilled.split()[-1]
