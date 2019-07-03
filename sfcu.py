import pickle
from driver import Driver, By
import time

def tonumber(s):
    return float(s[1:].replace(',', ''))

def read_hidden_value(browser, xpath):
    script = "return document.evaluate('" + xpath + "', document, null, XPathResult.ANY_TYPE, null).iterateNext().textContent;"
    return tonumber(browser.execute_script(script))

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
            current = tonumber(browser.find_elements_by_class_name('currency-debt')[-1].text)
            time.sleep(5); browser.wait_for('//div[contains(@class,"sidebar-content")]/div/div[2]')
            browser.click('//div[contains(@class,"tile-card-container")]/div[3]/div/div[1]')

            # read previous statement
            browser.wait_for('//div[contains(@class,"account-details ")]')
            previous = read_hidden_value(browser, '//div[contains(@class,"detail-tab-pane")]/dl/div[2]/dd/span')
            due = read_hidden_value(browser, '//div[contains(@class,"detail-tab-pane")]/dl/div[6]/dd/span')
            if due > 0:
                current -= previous

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

    return (str(previous), str(current))
