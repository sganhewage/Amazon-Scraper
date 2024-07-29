from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from amazoncaptcha import AmazonCaptcha
import datetime

from orderclass import Order

def scraping() -> None:
    email: str = "sganhewage1@gmail.com"
    password: str = input("Input Password: ")
    start_year: int = 2022

    driver = webdriver.Firefox()
    driver.get("https://www.amazon.com/gp/sign-in.html")

    #Ensure correct website
    assert "Amazon" in driver.title

    #CAPTCHA
    captcha = True
    try:
        text = driver.find_element(By.XPATH, "//h1[@class = 'a-spacing-small']").text
        if (text == "Sign in"): captcha = False
    except:
        pass
    if (captcha):
        captchaImageLink = driver.find_element(By.XPATH, "//div[@class = 'a-row a-text-center']//img").get_attribute('src')
        capthca_value = (AmazonCaptcha.fromlink(captchaImageLink)).solve()
        elem = driver.find_element(By.XPATH, "//div[@class = 'a-row a-spacing-base']//input")
        elem.send_keys(capthca_value)
        elem.send_keys(Keys.RETURN)

    #Enter email
    driver.get("https://www.amazon.com/gp/sign-in.html")
    elem = driver.find_element(By.ID, "ap_email")
    elem.send_keys(email)
    elem.send_keys(Keys.RETURN)

    #Wait for password page to load
    driver.implicitly_wait(5)

    #Enter password
    elem = driver.find_element(By.ID, "ap_password")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    #Go to orders and select current year
    ordersButton = driver.find_element(By.ID, "nav-orders")
    ordersButton.click()

    year: int = int(datetime.datetime.now().year)
    dropdown_option = 2
    #Get all orders
    orders = driver.find_elements(By.XPATH, "//div[@class = 'order-card js-order-card']")
    for order in orders:
        order.find_element(By.XPATH, "//span[@class = 'a-size-base a-color-secondary']")
        print(order.get_attribute('span'))
        # print(order.find_element(By.XPATH, "//div[@class = 'a-column a-span3']").text)

    while year >= (start_year+1):
        driver.implicitly_wait(5)
        elem = driver.find_element(By.ID, "a-autoid-1-announce")
        elem.click()

        buttonID = "time-filter_" + str(dropdown_option)
        driver.implicitly_wait(5)
        elem = driver.find_element(By.ID, buttonID)
        elem.click()

        year: int = int(driver.find_element(By.ID, "a-autoid-1-announce").find_element(By.CLASS_NAME, "a-dropdown-prompt").text)
        dropdown_option += 1

        new_orders = driver.find_elements(By.XPATH, "//div[@class = 'order-card js-order-card']")
        orders += new_orders

    print(orders.__len__())

if __name__ == "__main__":
    scraping()