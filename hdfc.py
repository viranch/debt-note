from driver import Driver, By

def get_unbilled(username, password):
    with Driver() as browser:
        logged_in = False
        try:
            # login
            print 'Logging in'
            browser.get('https://netbanking.hdfcbank.com/netbanking/')
            browser.switch_to.frame('login_page')
            browser.type_input(username, 'fldLoginUserId')
            browser.click('//img[@alt="continue"]')
            browser.type_input(password, 'fldPassword')
            browser.click('chkrsastu', by=By.NAME)
            browser.click('//img[@alt="Login"]')
            logged_in = True
            browser.wait_for('//frame[@name="main_part"]')

            # read unbilled message
            print 'Reading data'
            browser.switch_to.frame('main_part')
            unbilled = browser.wait_for('CCActiveMatSummary1', By.ID).text.split()[-1]
            browser.click('//img[@id="cclist"]/parent::a')
            browser.switch_to.frame('CC')
            billed = browser.wait_for('//table[@id="tab_id"]/tbody/tr[2]/td[2]').text.split()[-1]
        except:
            browser.get_screenshot_as_file('/tmp/{}_capture.png'.format(__name__))
            raise
        finally:
            if logged_in:
                browser.switch_to.default_content()
                # logout
                print 'Logging out'
                browser.switch_to.frame('common_menu1')
                browser.click('//img[@alt="Log Out"]')
                browser.wait_for('//body')

    return billed, unbilled
