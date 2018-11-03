from driver import Driver, By

def get_unbilled(username, password):
    with Driver() as browser:
        try:
            # login
            print 'Logging in'
            browser.get('https://global.americanexpress.com/login')
            browser.type_input(username, 'eliloUserID', By.ID)
            browser.type_input(password, 'eliloPassword', By.ID)
            browser.click('//button[@type="submit"]')

            # skip marketing modal
            print 'Reading data'
            browser.click('//section[@data-module-name="axp-marketing-offer"]//span[contains(@class, "dls-icon-close")]', timeout=5)

            # get balance details
            billed = browser.wait_for('//div[@class="summary-title"]/div[1]/div[2]/div/span').text.split()[-1]
            balance = browser.wait_for('//div[@class="summary-info"]/ul/li[2]/div/div[2]/div/span[1]').text.split()[1]
            unbilled = '{:,}'.format(float(balance.replace(',', '')) - float(billed.replace(',', '')))

            # logout
            print 'Logging out'
            browser.click('//button[contains(@class, "GlobalHeader__closed___35m2e")]')
            browser.wait_for('//body')
        except:
            browser.get_screenshot_as_file('/tmp/{}_capture.png'.format(__name__))
            raise

    return billed, unbilled
