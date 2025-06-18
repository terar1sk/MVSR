from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def main():
# 1) Настройка и запуск браузера
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # открывать окно в развернутом виде
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 300, poll_frequency=1)

# 2) Переходим на портал
    driver.get(
        "https://portal.minv.sk/wps/portal/domov/ecu/ecu_elektronicke_sluzby/"
        "ecu-vysys/!ut/p/a1/pZJbb4IwGIZ_yy64pW8rIOyu9dCCY45NI3KzaMKUTMAA078_"
        "IJrMHXCJ312b5-l36EciEpIoWx2SzapK8my1a86R9WpgMFLeBJ50eA-BJRg3p1MARg0sawB_"
        "BMelj2dzjIBKJXwJBoOd_A7gwrfVrH50MjaVEzz2IOl3_ydw4U99aoHP_ZngzpxBnusfSK6M_"
        "kPTkc3gDoUa9h0fcK3_9d-R4CYf5o3-1fwLErUIZcyl4qVG7MABl67VZyNBYdMrgIsT0DXDFuh"
        "aks5vaqbQDRjEI9Fml6_blV3ybN2zNyQq4re4iAv9o6ivt1W1L-81aDgej3qaZAe9fNfwG7_Ny4"
        "qEXzCyT-dthEjc5Cld2CW_-wTtu4K5/dl5/d5/L2dBISEvZ0FBIS9nQSEh/"
    )
    print("✅ Сайт запущен.")

# 3) Ждём, пока появится кнопка словацкого, и кликаем её
    btn_slovak = wait.until(
     EC.element_to_be_clickable((By.ID, "langSK"))
    )
    btn_slovak.click()
    print("✅ Нажатие кнопки выбора языка.")

# 4) Ждём, пока загрузится форма
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.reservation-data")))

# 5.1) Заполняем имя
    name_el = wait.until(EC.element_to_be_clickable((By.NAME, "s3-name-10")))
    name_el.clear()
    name_el.send_keys("Valeriia")
    print("✅ Поле имя заполнено.")

# 5.2) Заполняем фамилию
    surname_el = wait.until(EC.element_to_be_clickable((By.NAME, "s1-surname-10")))
    surname_el.clear()
    surname_el.send_keys("Terpai")
    print("✅ Поле фамилия заполнено.")

# 5.3) Заполняем фамилию
    surname_el = wait.until(EC.element_to_be_clickable((By.NAME, "s7-date-of-birth0")))
    surname_el.clear()
    surname_el.send_keys("30.11.2005")
    print("✅ Поле дата заполнено.")

# 5.4) Заполняем телефон
    phone_el = wait.until(EC.element_to_be_clickable((By.NAME, "s41-delivery-phone-captcha")))
    phone_el.clear()
    phone_el.send_keys("+421950318126")
    print("✅ Поле телефон заполнено.")

# 5.5) Заполняем e-mail
    email_el = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
    email_el.clear()
    email_el.send_keys("valeriiaterpai@gmail.com")
    print("✅ Поле e-mail заполнено.")

    print("✅ Поля имя, фамилия, дата, телефон и e-mail заполнены.")

# 6.1) Ждём, пока картинка капчи загрузится
    wait.until(EC.visibility_of_element_located((By.ID, "captchaImage")))
    print("🛑 На странице появилась капча. Введите её **полностью** в браузер в поле ‘answer’.")

    def has_captcha(drv):
        v = drv.find_element(By.NAME, "answer").get_attribute("value").strip()
        return len(v) >= 5

    wait.until(has_captcha)
    final = driver.find_element(By.NAME, "answer").get_attribute("value")
    print(f"✅ В поле капчи теперь: {final!r}. Скрипт продолжает работу.")

# 6.2) Кликаем кнопку «Odoslať» (отправить форму после капчи)
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "loadSecondFormButton")))
    submit_btn.click()
    print("✅ Нажата кнопка Odoslať")

# 7.1) Ждём появления поля для SMS-кода
    sms_field = wait.until(EC.element_to_be_clickable((By.ID, "pin-code")))
    print("🛑 Введите 6-значный код из SMS в поле на странице…")

# 7.2) Ждём, пока вы введёте ровно 6 цифр
    wait.until(lambda d: (
    val := d.find_element(By.ID, "pin-code").get_attribute("value").strip()
    ) and val.isdigit() and len(val) == 6)

# 7.3) Считаем введённое значение (на всякий случай)
    code = driver.find_element(By.ID, "pin-code").get_attribute("value")
    print(f"✅ Код из SMS введён: {code!r}")

# 7.4) Ждём и кликаем кнопку «Odoslať» (id="loadMain")
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "loadMain")))
    submit_btn.click()
    print("✅ Нажата кнопка Odoslať для подтверждения SMS-кода")

# 8.1) Ждём, пока в первом списке появится option с текстом "Prechodný pobyt"
    wait.until(EC.element_to_be_clickable((By.ID, "f1-life-situation-select1")))
    wait.until(EC.text_to_be_present_in_element(
        (By.ID, "f1-life-situation-select1"),
        "Prechodný pobyt"
    ))

    # Теперь выбираем “Prechodný pobyt”
    select1 = Select(driver.find_element(By.ID, "f1-life-situation-select1"))
    select1.select_by_visible_text("Prechodný pobyt")
    print("✅ Выбрано Prechodný pobyt в первом списке")

# 8.2) Ждём, пока во втором списке появятся нужные опции
    wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//select[@id='f1-life-situation-select2']/option[contains(text(),'Žiadosť o obnovenie prechodného pobytu')]"
    )))

# 8.3) Выбор «Situácie» → Žiadosť o obnovenie prechodného pobytu
    select2 = Select(driver.find_element(By.ID, "f1-life-situation-select2"))
    select2.select_by_visible_text("Žiadosť o obnovenie prechodného pobytu")
    print("✅ Выбрано Žiadosť o obnovenie prechodného pobytu во втором списке")

# 8.4) Ждём, пока появится fieldset для офиса (Pracoviská)
    wait.until(EC.visibility_of_element_located((By.ID, "f1-offices")))
    print("✅ Появился список офисов (Pracoviská).")

# 8.5) Ждём появления <label> с текстом "OCP Prešov"
    label_presov = wait.until(EC.visibility_of_element_located((
        By.XPATH,
        "//fieldset[@id='f1-offices']//label[normalize-space(text())='OCP Prešov']"
    )))
    # Получаем id связанного <input>
    input_id = label_presov.get_attribute("for")

# 8.6) Кликаем по найденному <input>
    radio_presov = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
    radio_presov.click()
    print("✅ Кликнули OCP Prešov")

# 8.7) Согласие на GDPR
    gdpr_chk = wait.until(EC.element_to_be_clickable((By.ID, "s42-check-gdpr-info")))
    if not gdpr_chk.is_selected():
        gdpr_chk.click()
    print("✅ Поставили галочку „Súhlasím so spracovaním osobných údajov“")

# 8.8) Выбор типа документа → Cudzinecký pas
    doc_select = Select(wait.until(EC.element_to_be_clickable((
        By.ID, "fs13-0-travel-doc-type"
    ))))
    doc_select.select_by_visible_text("Cudzinecký pas")
    print("✅ Выбрали Cudzinecký pas в списке dokumentov")

# 8.9) Ввод номера паспорта
    doc_num = wait.until(EC.element_to_be_clickable((By.ID, "fs13-travel-doc-number")))
    doc_num.clear()
    doc_num.send_keys("GC200401")
    print("✅ Ввели číslo dokladu: GC200401")



# 8.7) Ждём и кликаем кнопку «Odoslať» (id="loadMain") для перехода дальше
#    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "loadMain")))
#    submit_btn.click()
#    print("→ Нажали Odoslať, переходим к шагу 4")


# 100) Ждём от вас сигнала в консоли, чтобы закрыть браузер
    input("Браузер открылся и загрузил страницу. Нажмите Enter, чтобы закрыть…")
    driver.quit()


if __name__ == "__main__":
    main()