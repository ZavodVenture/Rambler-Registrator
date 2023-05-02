from random import randint, choice
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from threading import Thread
from configparser import ConfigParser
from time import time, sleep
from datetime import datetime
from string import ascii_letters, digits

busy_files = False

config = ConfigParser()
config.read('config.ini')


def chunks(lst, n):
    result = []
    for ind in range(0, len(lst), n):
        result.append(lst[ind:ind + n])

    return result


def tag(name: str, value: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Аккаунт {name}: " + value)


def worker(name):
    try:
        credentials = ''
        other_data = ''

        tag(name, 'запуск профиля...')

        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_argument('--disable-notifications')
        options.add_extension('extension.crx')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        tag(name, 'регистрация...')

        # CapMonsterCloud
        driver.get(f'chrome-extension://pabjfbciaedomjjfelfafejkppknjleh/popup.html')
        WebDriverWait(driver, 60).until(
            ec.presence_of_element_located((By.XPATH, '//input[@class="ant-input ant-input-sm"]'))).send_keys(
            config['settings']['cap_monster_api'])
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/button').click()

        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[2]/div/div[1]/div[1]/div/button').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[2]/div/div[5]/div[1]/div/button').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[2]/div/div[7]/div[1]/div/button').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[2]/div/div[2]/div/div/button').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[2]/div/div[4]/div/div/button').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[2]/div/div[6]/div[1]/div/button').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[2]/div/div[8]/div/div/button').click()

        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[2]/div/div[3]/div[2]').click()
        sleep(2)

        driver.execute_script(
            "document.getElementsByClassName('ant-radio-button-wrapper sc-1kl07qn bPqmGH')[0].click()")

        # Rambler
        driver.get('https://mail.rambler.ru/')
        iframe = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/iframe')))
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/footer/div/a'))).click()

        start = time()
        while 1:
            if time() - start >= 30:
                raise
            try:
                nickname = requests.post('https://rustxt.ru/api/index.php',
                                         data={'method': 'getNickName', 'count_result': 1, 'len_nick_min': 7,
                                               'len_nick_max': 10}).json()[0] + str(randint(111, 999))
            except:
                continue
            else:
                if not nickname:
                    continue

            sleep(1)
            WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="reg_login"]'))).send_keys(
                nickname)
            try:
                WebDriverWait(driver, 2).until(ec.presence_of_element_located(
                    (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div/div/div[1]/form/section[1]/div/div/div[2]')))
            except:
                credentials += f'{nickname}@rambler.ru:'
                break

        password = ''.join([choice(ascii_letters + digits) for i in range(20)]) + choice(digits)
        credentials += password + '\n'
        el = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, '//*[@id="reg_new_password"]')))
        el.click()
        el.send_keys(password)
        el = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="reg_confirm_password"]')))
        el.click()
        el.send_keys(password)

        driver.find_element(By.XPATH,
                            '//*[@id="__next"]/div/div/div[2]/div/div/div/div[1]/form/section[4]/div/div/div[1]/div/div/div/input').click()
        driver.find_elements(By.XPATH,
                                         '//*[@id="__next"]/div/div/div[2]/div/div/div/div[1]/form/section[4]/div/div/div[1]/div/div[2]/div/div/div[1]/div/div/div')[0].click()
        answer = str(randint(11111, 99999))
        driver.find_element(By.XPATH, '//*[@id="reg_answer"]').send_keys(answer)

        WebDriverWait(driver, 999).until(ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div/div/div[1]/form/button'))).click()

        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/footer/div/a').click()
        driver.switch_to.default_content()
        sleep(5)

        driver.get('https://mail.rambler.ru/settings/mailapps')
        try:
            WebDriverWait(driver, 3).until(
                ec.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/button[1]'))).click()
        except:
            pass

        WebDriverWait(driver, 60).until(ec.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="app"]/div[2]/div[4]/div[2]/div[2]/div[1]/div/div[3]/div[1]/div/div/button[1]'))).click()

        start = time()
        while 1:
            script = "return document.getElementsByClassName('rui-Button-button rui-Button-type-primary rui-Button-size-small rui-Button-iconPosition-left MailAppsChange-submitButton-S7')[0].disabled"
            status = driver.execute_script(script)
            if not status:
                script = "document.getElementsByClassName('rui-Button-button rui-Button-type-primary rui-Button-size-small rui-Button-iconPosition-left MailAppsChange-submitButton-S7')[0].click()"
                driver.execute_script(script)
                break
            if time() - start >= 999:
                raise
            sleep(0.5)

        sleep(5)
        driver.close()

        other_data += f'Answer: {answer}\n'

        global busy_files
        while 1:
            if not busy_files:
                busy_files = True
                break

        with open('credentials.txt', 'a', encoding='utf-8') as file:
            file.write(credentials)
            file.close()
        with open('other_data.txt', 'a', encoding='utf-8') as file:
            file.write(other_data)
            file.close()
        busy_files = False

        tag(name, 'регистрация завершена')
    except Exception:
        tag(name, f'произошла непредвиденная ошибка')


if __name__ == '__main__':
    accounts_number = int(config['settings']['accounts_number'])
    threads_number = int(config['settings']['threads_number'])

    accounts = [Thread(target=worker, args=(number,)) for number in range(accounts_number)]
    groups = chunks(accounts, threads_number)

    for group in groups:
        for thread in group:
            thread.start()
        for thread in group:
            thread.join()
