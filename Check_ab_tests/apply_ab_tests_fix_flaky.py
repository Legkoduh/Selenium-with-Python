from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import re


def change_cookie(driver, cookie):
    valid_ab_test_cookie = cookie
    valid_ab_test_cookie['value'] = '9'
    driver.delete_cookie("_pc_PianoABtestv2")
    driver.add_cookie(valid_ab_test_cookie)
    driver.refresh()


def refresh_empty_widget(driver, wait, ac, ec, widget_locator):
    rec_latest_news_widget = None
    for _ in range(5):
        driver.refresh()
        try:
            rec_latest_news_widget = wait.until(ec.visibility_of_element_located(widget_locator))
            ac.scroll_to_element(rec_latest_news_widget).perform()
            break
        except TimeoutException:
            refresh_empty_widget(driver, wait, ac, ec, widget_locator)
        except StaleElementReferenceException:
            ac.scroll_to_element(rec_latest_news_widget).perform()

    return


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
        try:
            rec_latest_news_widget = wait.until(ec.visibility_of_element_located(REC_LATEST_NEWS_WIDGET))
            ac.scroll_to_element(rec_latest_news_widget).perform()
        except TimeoutException:
            edition = re.sub(r"[:/.]", '', link[8:])
            WIDGET_MORE_BUTTON = ('xpath', "//div[@class='ms-items-widget__more-bottom']")
            widget_more_button = driver.find_element(*WIDGET_MORE_BUTTON)
            height = widget_more_button.location['y'] - 250
            driver.execute_script(f"window.scrollTo(0, {height});")
            driver.save_screenshot(f"./screenshots/{edition}_widget_empty.png")
            refresh_empty_widget(driver, wait, ac, ec, REC_LATEST_NEWS_WIDGET)
        except StaleElementReferenceException:
            refresh_empty_widget(driver, wait, ac, ec, REC_LATEST_NEWS_WIDGET)

    REC_NEWS_LIST = ('xpath', "//msnt-home-latest-news[@data-widget='latest-news']//a[contains(@class, 'msnt-froomle-item msnt-item-abtest-candidate')]")
    try:
        rec_news_list = wait.until(ec.visibility_of_all_elements_located(REC_NEWS_LIST))
    except TimeoutException:
        rec_news_list = wait.until(ec.visibility_of_all_elements_located(REC_NEWS_LIST))


    driver.quit()

    return len(rec_news_list)
