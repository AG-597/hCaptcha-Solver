import time
import base64
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import requests
from tensorflow.keras.applications import MobileNetV2

TF_ENABLE_ONEDNN_OPTS = 0

custom_objects = {'MobileNetV2': MobileNetV2}

loaded_model = load_model('model.keras', custom_objects=custom_objects)
loaded_model.summary()

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def predict_image_class(img_path):
    img_array = preprocess_image(img_path)
    predictions = loaded_model.predict(img_array)
    predicted_class_index = np.argmax(predictions)
    return predicted_class_index

driver = Driver(uc=True)
driver.get('https://accounts.hcaptcha.com/demo')
wait = WebDriverWait(driver, 10)

def is_captcha_present():
    driver.switch_to.default_content()
    if len(driver.find_elements(By.XPATH,"//iframe[contains(@src,'hcaptcha') and contains(@src,'checkbox')]")) == 0:
        return False
    
    if driver.find_element(By.XPATH,"//iframe[contains(@src,'hcaptcha') and contains(@src,'checkbox')]").is_displayed():
        return True
    else:
        return False
    
def is_challenge_present():
    driver.switch_to.default_content()
    if len(driver.find_elements(By.XPATH,"//iframe[contains(@src,'hcaptcha') and contains(@src,'challenge')]")) == 0:
        return False
    
    if driver.find_element(By.XPATH,"//iframe[contains(@src,'hcaptcha') and contains(@src,'challenge')]").is_displayed():
        return True
    else:
        return False
    
def launch_captcha():
    if not is_captcha_present():
        raise Exception("No hCaptcha challenge box present")
    launched = False
    
    driver.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@src,'hcaptcha') and contains(@src,'checkbox')]")))
    launch = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body")))
    try:
        launch.click()
    except:
        driver.execute_script("arguments[0].click()", launch)


def get_number_of_crumbs():
    if not is_challenge_present():
        raise Exception("No hCaptcha challenge box present")
    
    driver.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@src,'hcaptcha') and contains(@src,'challenge')]")))
    return max(len(driver.find_elements(By.XPATH, "//div[@class='Crumb']")),1)

def refresh_all_v2():
    driver.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@src,'hcaptcha') and contains(@src,'challenge')]")))
    
    while driver.find_elements(By.XPATH, "//h2[@class='prompt-text']") == []:
        time.sleep(0.1)

    captcha_strs = driver.find_elements(By.XPATH, "//h2[@class='prompt-text']/span")
    if captcha_strs == []:
        refresh_challenge()
        time.sleep(0.5)
        refresh_all_v2()

def refresh_challenge():
    driver.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@src,'hcaptcha') and contains(@src,'challenge')]")))

    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'refresh button')]"))).click()

    time.sleep(2)

def get_challenge_data():
    driver.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@src,'hcaptcha') and contains(@src,'challenge')]")))

    try:
        captcha_str = driver.find_element(By.XPATH, "//h2[@class='prompt-text']/span").text
    except:
        try: 
            captcha_str = driver.find_element(By.XPATH, "//h2[@class='prompt-text']").text
        except:
            refresh_challenge()
            time.sleep(0.5)
            refresh_all_v2()
            captcha_str = driver.find_element(By.XPATH, "//h2[@class='prompt-text']/span").text

    image_divs = driver.find_elements(By.XPATH, "//div[contains(text(), 'click')]")  # challenge images
    while True:
        try:
            image_style_strs = [image_div.get_attribute("style") for image_div in image_divs]
            break
        except:
            continue
    while True:
        try:
            urls = [image_style_str.split("url(\"")[1].split("\") ")[0] for image_style_str in image_style_strs]
            break
        except:
            continue

    return captcha_str, urls

def abort():
    driver.switch_to.default_content()
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body"))).click()

def click_correct():
    captcha_str, image_urls = get_challenge_data()

    while True:
        if "containing a streetlamp" in captcha_str:
            class_index = 37
            break
        elif "flying vehicle" in captcha_str:
            class_index = 0
            break
        elif "without animals" in captcha_str:
            class_index = 68
            break
        elif "frozen liquid" in captcha_str:
            class_index = 3
            break
        elif "usually wears a crown" in captcha_str:
            class_index = 79
            break
        else:
            refresh_challenge()
            continue
        
    driver.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@src,'hcaptcha') and contains(@src,'challenge')]")))
        
    image_divs = driver.find_elements(By.XPATH, "//div[@class='border']")

    for image_url in image_urls:
        response = requests.get(image_url)
        img_binary = response.content
        img_path = 'temp_image.png'
        print(image_url)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_binary)
        
        predicted_class_index = predict_image_class(img_path)
        print(predicted_class_index)
        
        for img in image_divs:
            #if predicted_class_index == class_index:
                driver.execute_script("arguments[0].click();", img)
                time.sleep(0.5)

launch_captcha()
click_correct()
time.sleep(100)