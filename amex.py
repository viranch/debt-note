from selenium.webdriver.common.by import By
from driver import Driver

class AMEX(object):
    def __init__(self):
        self.driver = Driver()

    def get_unbilled(self, username, password):
        # login
        print 'Logging in'
        self.driver.get('https://global.americanexpress.com/myca/logon/japa/action?request_type=LogonHandler&Face=en_IN')
        self.driver.type_input(username, 'UserID')
        self.driver.type_input(password, 'Password')
        self.driver.click('//a[@alt="Log in to Online Services"]')

        # skip marketing modal
        print 'Reading data'
        self.driver.click('//section[data-module-name="axp-marketing-offer"]//span[contains(@class, "dls-icon-close")]', timeout=5)

        # get balance details
        self.driver.click('//button[@title="Balance & Credit Details"]')
        unbilled = self.driver.wait_for('//table[@class="balance-details-list"]/tbody/tr[4]/td[3]/span').text
        self.driver.click('//header[@role="heading"]/span/button')
        self.driver.wait_for_invisibility('//header[@role="heading"]')

        # logout
        print 'Logging out'
        self.driver.click('//button[contains(@class, "GlobalHeader__closed___35m2e")]')
        self.driver.wait_for('//body')
        self.driver.quit()

        return unbilled.split()[-1]
