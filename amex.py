from driver import Driver, By

def get_unbilled(username, password):
    with Driver() as browser:
        # login
        print 'Logging in'
        browser.get('https://global.americanexpress.com/myca/logon/japa/action?request_type=LogonHandler&Face=en_IN')
        browser.type_input(username, 'UserID')
        browser.type_input(password, 'Password')
        browser.click('//a[@alt="Log in to Online Services"]')

        # skip marketing modal
        print 'Reading data'
        browser.click('//section[data-module-name="axp-marketing-offer"]//span[contains(@class, "dls-icon-close")]', timeout=5)

        # get balance details
        unbilled = browser.wait_for('//div[@class="summary-info"]/ul/li[2]//div[@class="data-value"]/span').text

        # logout
        print 'Logging out'
        browser.click('//button[contains(@class, "GlobalHeader__closed___35m2e")]')
        browser.wait_for('//body')

    return unbilled.split()[-1]
