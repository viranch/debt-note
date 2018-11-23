import pickle
from driver import Driver, By

def get_unbilled(username, password):
    login_url = 'https://e.sfcu.org/sfcuonline/uux.aspx#/login'
    with Driver() as browser:
        try:
            # login
            print 'Logging in'
            browser.get(login_url)
            browser.load_cookies(__name__)
            browser.type_input(username, 'fldUsername', by=By.ID)
            browser.type_input(password, 'fldPassword', by=By.ID)
            browser.click('//button[@test-id="btnSubmit"]')

            # read balance
            print 'Reading data'
            browser.wait_for('//*[contains(@class, "currency-debt")]', timeout=30)
            balance = browser.find_elements_by_class_name('currency-debt')[-1].text[1:]
        except:
            browser.get_screenshot_as_file('/tmp/{}_capture.png'.format(__name__))
            raise
        finally:
            print 'Logging out'
            browser.click('//a[contains(@class, "logoff")]')
            browser.wait_for_invisibility('//span[@class="customer-name"]')
            browser.wait_for('//body')
            browser.get(login_url)
            browser.wait_for('//body')
            browser.dump_cookies(__name__)

    return (None, balance)
