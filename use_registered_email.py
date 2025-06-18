def use_registered_email_address(preconds, edition):
    driver, wait_for, exp_conds, ac_chains = preconds

    driver.get(edition)

    if edition != 'https://motor1.uol.com.br/' and edition != 'https://insideevs.uol.com.br/':
        IFRAME = ('xpath', "//iframe[@title='Iframe title']")
        iframe = wait_for.until(exp_conds.visibility_of_element_located(IFRAME))

        driver.switch_to.frame(iframe)
        ACCEPT_BUTTON = ('xpath', "//div[@class='message-component message-row row-consent']//button")
        driver.find_element(*ACCEPT_BUTTON).click()

        wait_for.until(exp_conds.invisibility_of_element(iframe))
        driver.switch_to.default_content()


    SIGN_IN_ICON = ('xpath', "//div[contains(@class, 'user_avatar user_avatar-desktop')]")

    ac_chains.move_to_element(driver.find_element(*SIGN_IN_ICON)).click().perform()

    # Sign in block disappears immediately with this implementation
    # dr.find_element(*SIGN_IN_ICON).click()

    SIGN_IN_BLOCK = ('xpath', "//div[@class='m1-desktop-registration']")
    sign_in_block = wait_for.until(exp_conds.visibility_of_element_located(SIGN_IN_BLOCK))

    SIGN_IN_BUTTON = ('xpath', "//a[@class='login']")
    sign_in_button = wait_for.until(exp_conds.visibility_of_element_located(SIGN_IN_BUTTON))
    sign_in_button.click()

    SING_IN_FORM = ('xpath', "//div[contains(@class, 'loginFormWrapper')]")
    sign_in_form = wait_for.until(exp_conds.visibility_of_element_located(SING_IN_FORM))

    # Or use this locator
    # EMAIL_FIELD = ('xpath', "//div[@class='form-input-wrapper']/input")
    EMAIL_FIELD = ('xpath', "//input[@placeholder='automotive.fan@gmail.com']")
    email_field = driver.find_element(*EMAIL_FIELD)
    email_field.send_keys("test@gmail.com")

    LOGIN_BUTTON = ('xpath', "//form[@name='sign_in_form']//input[@type='submit']")
    login_button = driver.find_element(*LOGIN_BUTTON)
    login_button.click()

    PASSWORD_FIELD = ('xpath', "//input[@type='password']")
    password_field = wait_for.until(exp_conds.visibility_of_element_located(PASSWORD_FIELD))
    password_field_visible = password_field.is_displayed()

    driver.quit()

    return password_field_visible
