def change_cookie(driver, cookie):
    valid_ab_test_cookie = cookie
    valid_ab_test_cookie['value'] = '9'
    driver.delete_cookie("_pc_PianoABtestv2")
    driver.add_cookie(valid_ab_test_cookie)
    driver.refresh()


def check_ab_tests(driver, wait, ec, ac, link, cookie_value):

    driver.get(link)

    CONSENT_IFRAME = ("xpath", "//iframe[contains(@id, 'sp_message_iframe_')]")
    consent_iframe = wait.until(ec.visibility_of_element_located(CONSENT_IFRAME))
    driver.switch_to.frame(consent_iframe)
    if link[:10] != 'https://nl':
        ACCEPT_BUTTON = ("xpath", "//button[contains(@class, 'sp_choice_type_ACCEPT_ALL')]")
    else:
        ACCEPT_BUTTON = ("xpath", "//div[@class='message-component message-row consent-body-buttons-wrapper']/p")

    accept_button = driver.find_element(*ACCEPT_BUTTON)
    accept_button.click()
    driver.switch_to.default_content()

    ab_test_cookie = driver.get_cookie("_pc_PianoABtestv2")

    if int(ab_test_cookie['value']) < cookie_value:
        change_cookie(driver, ab_test_cookie)

        DEFAULT_LATEST_NEWS_WIDGET = ('xpath', "//msnt-home-latest-news[@data-widget='latest-news']/div[3]/a/div")
        default_latest_news_widget = wait.until(ec.visibility_of_element_located(DEFAULT_LATEST_NEWS_WIDGET))
        ac.scroll_to_element(default_latest_news_widget).perform()
        REC_BUTTON = ("xpath", "//msnt-toggle-button-group[contains(@class, 'msnt-toggle-button-group')]/button[2]")
        rec_button = driver.find_element(*REC_BUTTON)
        rec_button.click()
    else:
        REC_LATEST_NEWS_WIDGET = ("xpath", "//msnt-home-latest-news[@data-widget='latest-news']/div[4]/a/div")
        rec_latest_news_widget = wait.until(ec.visibility_of_element_located(REC_LATEST_NEWS_WIDGET))
        ac.scroll_to_element(rec_latest_news_widget).perform()

    REC_NEWS_LIST = ('xpath', "//msnt-home-latest-news[@data-widget='latest-news']//a[contains(@class, 'msnt-froomle-item msnt-item-abtest-candidate')]")
    rec_news_list = wait.until(ec.visibility_of_all_elements_located(REC_NEWS_LIST))

    driver.quit()

    return len(rec_news_list)
