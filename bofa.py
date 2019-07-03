from driver import Driver, By, TimeoutException

def tonumber(browser, xpath):
    return float(browser.wait_for(xpath).text[1:].replace(',', ''))

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
            browser.click('//div[contains(@class,"AccountItemCreditCard")]//a[@name="CCA_details"]')
            current = tonumber(browser, '//div[contains(@class,"summary-acct-row")][1]/div[2]')
            previous = tonumber(browser, '//div[contains(@class,"statement-details")]/div[contains(@class,"ptc-row")][1]/div[2]')
            due = tonumber(browser, '//div[contains(@class,"statement-details")]/div[contains(@class,"ptc-row")][last()]/div[2]')
            if due > 0:
                current -= previous
        except:
            browser.get_screenshot_as_file('/tmp/{}_capture.png'.format(__name__))
            raise
        finally:
            print 'Logging out'
            browser.click('//a[@name="onh_sign_off"]')
            browser.wait_for('//body')
            browser.get(login_url)
            browser.wait_for('//body')
            browser.dump_cookies(__name__)

    return (str(previous), str(current))
