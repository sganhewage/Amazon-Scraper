from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from amazoncaptcha import AmazonCaptcha
import datetime

from orderclass import Order

def scraping() -> None:
    email: str = "sganhewage1@gmail.com"
    password: str = input("Input Password: ")
    start_year: int = 2024

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

    # Get all orders
    orders = []
    while year >= (start_year):
        driver.implicitly_wait(5)            
        elem = driver.find_element(By.ID, "a-autoid-1-announce")
        elem.click()

        buttonID = "time-filter_" + str(dropdown_option)
        driver.implicitly_wait(5)
        elem = driver.find_element(By.ID, buttonID)
        elem.click()
        
        driver.implicitly_wait(5)
        numPages = driver.find_elements(By.CLASS_NAME, "a-normal").__len__() + 1
        print(numPages)
        for i in range(numPages):
            orderElements = driver.find_elements(By.XPATH, "//div[@class = 'order-card js-order-card']")
            for order in orderElements:
                orders.append(str(order.find_element(By.CLASS_NAME, "a-link-normal").get_attribute('href')))
            nextButton = driver.find_element(By.CLASS_NAME, "a-last")
            nextButton.click()
            driver.implicitly_wait(5)

        year: int = int(driver.find_element(By.ID, "a-autoid-1-announce").find_element(By.CLASS_NAME, "a-dropdown-prompt").text)-1
        dropdown_option += 1

    orders = list(set(orders))
    print(orders.__len__())
    
    # Grab Order Information
    for order in orders:
        driver.get(order)
        driver.implicitly_wait(5)
        
        # Order Number
        orderNumber = driver.find_element(By.XPATH, "//span[@class = 'order-date-invoice-item']//bdi").text
        print(orderNumber)
        
        # Order Date
        orderDate = driver.find_element(By.XPATH, "//span[@class = 'order-date-invoice-item']").text
        orderDate = orderDate[11:]
        print(orderDate)
        
        # Order Grand Total
        orderTotal = driver.find_element(By.XPATH, "//div[@class = 'a-column a-span5 a-text-right a-span-last']//span[@class = 'a-color-base a-text-bold']").text
        print(orderTotal)
        
        # Payment Method
        paymentMethod = driver.find_element(By.XPATH, "//div[@class = 'a-row pmts-payments-instrument-details']//span[@class = 'a-list-item']").text
        print(paymentMethod)
        
        # Shipping Address
        AddressLine1 = driver.find_element(By.XPATH, "//div[@class = 'displayAddressDiv']//li[@class = 'displayAddressLI displayAddressAddressLine1']").text
        cityStateZip = driver.find_element(By.XPATH, "//div[@class = 'displayAddressDiv']//li[@class = 'displayAddressLI displayAddressCityStateOrRegionPostalCode']").text
        country = driver.find_element(By.XPATH, "//div[@class = 'displayAddressDiv']//li[@class = 'displayAddressLI displayAddressCountryName']").text
        shippingAddress = AddressLine1 + ", " + cityStateZip + ", " + country
        print(shippingAddress)
        
        # Loop following attributes
        
        # Item Image
        itemImage = driver.find_element(By.CLASS_NAME, "yo-critical-feature").get_attribute('src')
        print(itemImage)
        
        # Total Before Tax
        totalBeforeTax = driver.find_element(By.XPATH, "//span[@class = 'a-size-small a-color-price']").text
        print(totalBeforeTax)
        
        # Item Name
        itemName = driver.find_element(By.XPATH, "//div[@class = 'a-fixed-left-grid-inner']//div[@class = 'a-row']//a[@class = 'a-link-normal']").text
        print(itemName)
        
        # URL
        url = driver.find_element(By.XPATH, "//div[@class = 'a-fixed-left-grid-inner']//div[@class = 'a-row']//a[@class = 'a-link-normal']").get_attribute('href')
        print(url)
        
        # Seller
        seller = driver.find_element(By.XPATH, "//div[@class = 'a-fixed-left-grid-inner']//span[@class = 'a-size-small a-color-secondary']").text
        seller = seller[9:]
        print(seller)
        
        # Delivery Date / Status
        infoAvailable = True
        try:
            deliveryDate = driver.find_element(By.XPATH, "//span[@class = 'a-size-medium a-color-base a-text-bold']").text
        except:
            try:
                deliveryDate = driver.find_element(By.XPATH, "//span[@class = 'a-size-medium a-text-bold']").text
            except:
                infoAvailable = False
            
        if (infoAvailable):
            if (deliveryDate.__contains__("Return")):
                deliveryDate = "Returned"
                status = "Returned"
            elif (deliveryDate.__contains__("Replace")):
                deliveryDate = "Replaced"
                status = "Replaced"
            elif (deliveryDate.__contains__("Delivered")):
                deliveryDate = deliveryDate[10:]
                status = "Delivered"
            elif (deliveryDate.__contains__("Arriving")):
                deliveryDate = deliveryDate[9:]
                status = "In Transit"
        else:
            deliveryDate = "Unavailable"
            status = "N/A"
        print(deliveryDate)
        print(status)        
        
        
        

if __name__ == "__main__":
    scraping()