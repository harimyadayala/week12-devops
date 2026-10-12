
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def fill_form(driver, name, student_id, email, year):
    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "student_id").send_keys(student_id)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "year").send_keys(year)


def test_empty_name(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    fill_form(driver, "", "ST101", "student@gmail.com", "3rd Year")

    button = driver.find_element(By.NAME, "sb")
    assert driver.find_element(By.NAME, "name").get_attribute("required") is not None
    assert driver.find_element(By.NAME, "name").get_attribute("value") == ""
    assert button.is_displayed()


def test_empty_student_id(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    fill_form(driver, "Harimya", "", "student@gmail.com", "3rd Year")

    student_id = driver.find_element(By.NAME, "student_id")
    assert student_id.get_attribute("required") is not None
    assert student_id.get_attribute("value") == ""


def test_invalid_email(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    fill_form(driver, "Harimya", "ST101", "invalid-email", "3rd Year")

    email = driver.find_element(By.NAME, "email")
    is_valid = driver.execute_script(
        "return arguments[0].checkValidity();", email
    )
    assert is_valid is False


def test_valid_registration(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    fill_form(
        driver,
        "Harimya",
        "ST101",
        "harimya@gmail.com",
        "3rd Year"
    )

    driver.find_element(By.NAME, "sb").click()

    WebDriverWait(driver, 10).until(
        lambda d: "/register" in d.current_url
    )

    assert "Student Registration Successful!" in driver.page_source
    assert "Harimya" in driver.page_source
    assert "ST101" in driver.page_source
    assert "harimya@gmail.com" in driver.page_source
    assert "3rd Year" in driver.page_source
