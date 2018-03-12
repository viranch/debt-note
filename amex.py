from driver import Driver, By

def get_unbilled(username, password):
    with Driver() as browser:
        try:
            # login
            print 'Logging in'
            browser.get('https://global.americanexpress.com/myca/logon/japa/action?request_type=LogonHandler&Face=en_IN')
            browser.type_input(username, 'UserID')
            browser.type_input(password, 'Password')
            browser.click('//a[@alt="Log in to Online Services"]')

            # skip marketing modal
            print 'Reading data'
            browser.click('//section[@data-module-name="axp-marketing-offer"]//span[contains(@class, "dls-icon-close")]', timeout=5)

            # get balance details
            billed = browser.wait_for('//div[@class="summary-title"]/div[1]/div[2]/div/span').text.split()[-1]
            unbilled = browser.wait_for('//section[@id="recent-activity"]/div[1]/div[2]/p').text.split()[1]

            # logout
            print 'Logging out'
            browser.click('//button[contains(@class, "GlobalHeader__closed___35m2e")]')
            browser.wait_for('//body')
        except:
            browser.get_screenshot_as_file('/tmp/amex_capture.png')
            raise

    return billed, unbilled
