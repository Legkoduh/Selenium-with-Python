from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from apply_ab_tests_fix_flaky import check_ab_tests
import pytest


links_cookies = [('https://www.autosport.com/', 9), ('https://www.motorsport.com/', 9), ('https://fr.motorsport.com/', 2),
                 ('https://es.motorsport.com/', 9), ('https://it.motorsport.com/', 9), ('https://nl.motorsport.com/', 2),
                 ('https://www.autosport.com/f1/', 9), ('https://www.motorsport.com/f1/', 9), ('https://fr.motorsport.com/f1/', 2),
                 ('https://es.motorsport.com/f1/', 9), ('https://it.motorsport.com/f1/', 9), ('https://nl.motorsport.com/f1/', 2)]



@pytest.mark.parametrize(
    ('link', 'value'),
    links_cookies
)
def test_ab_tests(link, value):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options)
    wait = WebDriverWait(driver, 15)
    ec = expected_conditions
    ac = ActionChains(driver)
    assert 20 == check_ab_tests(driver, wait, ec, ac, link, value)
