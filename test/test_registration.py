
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
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
    driver.find_element(By.NAME, "sb").click()

    assert driver.current_url.endswith("/")
    assert driver.find_element(By.NAME, "name").get_attribute("required") is not None


def test_empty_student_id(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    fill_form(driver, "Harimya", "", "student@gmail.com", "3rd Year")
    driver.find_element(By.NAME, "sb").click()

    assert driver.current_url.endswith("/")
    assert driver.find_element(By.NAME, "student_id").get_attribute("required") is not None


def test_invalid_email(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    fill_form(driver, "Harimya", "ST101", "invalid-email", "3rd Year")
    driver.find_element(By.NAME, "sb").click()

    assert driver.current_url.endswith("/")
    assert driver.find_element(By.NAME, "email").get_attribute("type") == "email"


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

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/register"))

    body_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Student Registration Successful!" in body_text
    assert "Harimya" in body_text
    assert "ST101" in body_text
    assert "harimya@gmail.com" in body_text
    assert "3rd Year" in body_text
