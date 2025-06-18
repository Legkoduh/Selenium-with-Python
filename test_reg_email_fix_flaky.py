from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
import pytest
from use_reg_email_with_fix_flaky import use_registered_email_address



editions_m1 = ['https://www.motor1.com/', 'https://fr.motor1.com/', 'https://it.motor1.com/', 'https://de.motor1.com/',
               'https://es.motor1.com/', 'https://ar.motor1.com/', 'https://tr.motor1.com/', 'https://motor1.uol.com.br/',
               'https://id.motor1.com/', 'https://me.motor1.com/']

editions_ev = ['https://insideevs.com/', 'https://insideevs.fr/', 'https://insideevs.it/', 'https://insideevs.uol.com.br/',
               'https://insideevs.de/', 'https://insideevs.com.tr/', 'https://insideevs.com.ar/']

editions_other = ['https://www.rideapart.com/', 'https://www.omnitrattore.it/']


@pytest.fixture
def preconds():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options)
    wait = WebDriverWait(driver, 15)
    ec = expected_conditions
    ac = ActionChains(driver)

    yield (driver, wait, ec, ac)
    driver.quit()


@pytest.mark.parametrize(
    ("edition"),
    editions_m1 + editions_ev + editions_other
)
def test_registered_email_address(preconds, edition):
    assert use_registered_email_address(preconds, edition) == True
