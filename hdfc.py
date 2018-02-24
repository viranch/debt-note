from driver import Driver, By

def get_unbilled(username, password):
    with Driver() as browser:
        # login
        print 'Logging in'
        browser.get('https://netbanking.hdfcbank.com/netbanking/')
        browser.switch_to.frame('login_page')
        browser.type_input(username, 'fldLoginUserId')
        browser.click('//img[@alt="continue"]')
        browser.type_input(password, 'fldPassword')
        browser.click('chkrsastu', by=By.NAME)
        browser.click('//img[@alt="Login"]')
        browser.wait_for('//frame[@name="main_part"]')

        # read unbilled message
        print 'Reading data'
        browser.switch_to.frame('main_part')
        unbilled = browser.wait_for('CCActiveMatSummary1', By.ID).text.split()[-1]
        browser.click('//img[@id="cclist"]/parent::a')
        browser.switch_to.frame('CC')
        billed = browser.wait_for('//table[@id="tab_id"]/tbody/tr[2]/td[2]').text.split()[-1]
        browser.switch_to.default_content()

        # logout
        print 'Logging out'
        browser.switch_to.frame('common_menu1')
        browser.click('//img[@alt="Log Out"]')
        browser.wait_for('//body')

    return billed, unbilled
