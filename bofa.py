from driver import Driver, By

def get_unbilled(username, password):
    login_url = 'https://secure.bankofamerica.com/login/sign-in/signOnV2Screen.go'
    with Driver() as browser:
        try:
            # login
            print 'Logging in'
            browser.get(login_url)
            browser.load_cookies(__name__)
            browser.type_input(username, 'dummy-onlineId')
            browser.type_input(password, 'dummy-passcode')
            browser.click('enter-online-id-submit', by=By.NAME)

            # read balance
            print 'Reading data'
            balance = browser.wait_for('//div[contains(@class,"AccountItemCreditCard")]/div[contains(@class,"AccountBalance")]/span').text[1:]
        except:
            browser.get_screenshot_as_file('/tmp/{}_capture.png'.format(__name__))
            raise
        finally:
            print 'Logging out'
            browser.get('https://secure.bankofamerica.com/myaccounts/signoff/signoff-default.go')
            browser.wait_for('//h1[text()="Signing Out"]')
            browser.wait_for_invisibility('//h1[text()="Signing Out"]')
            browser.wait_for('//body')
            browser.get(login_url)
            browser.wait_for('//body')
            browser.dump_cookies(__name__)

    return (None, balance)
