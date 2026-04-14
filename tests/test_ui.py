import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import allure
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from pages.ui_class import UiPage
load_dotenv()

base_url = os.getenv("BASE_URL")


@allure.title("Тест проверки кнопок бесплатного доступа")
@allure.description(
    "Проверяет функциональность кнопок бесплатного доступа на сайте:"
    "переход по кнопкам, проверку текста на кнопках и соответствие URL.")
@allure.feature("Бесплатный доступ")
@allure.severity(allure.severity_level.NORMAL)
def test_buttons_free(driver)  -> None:
    """
    Тест проверки кнопок бесплатного доступа.

    Args:
        driver: из фикстуры driver.

    Returns:
        None: Тест не возвращает значение,
        выполняет проверки через assert.
    """
    o_c_b: str = os.getenv("OCB")
    i_c_s: str = os.getenv("ICS")
    find_b: str = os.getenv("FIND_B")
    btn_k_m: str = os.getenv("BTN_KM")
    page: UiPage = UiPage(driver, base_url)

    with allure.step("Открыть сайт"):
        page.open_site()

    with allure.step("Пройти капчу"):
        page.capcha()

    with allure.step("Нажать на кнопку 'Онлайн-кинотеатр'"):
        page.search_by_xpath(o_c_b)
        page.click_element(o_c_b, by=By.XPATH)

    with allure.step(
            "Проверить видимость элемента с текстом '30 дней бесплатно'"):
        i_can_see = page.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, i_c_s))
        )
        with allure.step(
                "Проверить, что в тексте элемента есть"
                "'30 дней бесплатно'"):
            assert "30 дней бесплатно" in i_can_see.text

    with allure.step(
            "Найти кнопку 'Смотреть бесплатно'"
            "и проверить текст на ней"):
        find_button = page.search_by_css(find_b)
        text_on_button: str = find_button.text
        with allure.step(
                "Ожидаемый текст на кнопке: 'Попробовать бесплатно'"):
            assert text_on_button == "Попробовать бесплатно"
    with allure.step("Нажать на кнопку 'Попробовать бесплатно'"):
        page.click_element(find_b, by=By.CSS_SELECTOR)

    with allure.step("Нажать на кнопку 'Узнать больше'"):
        page.search_by_css(btn_k_m)
        page.click_element(btn_k_m, by=By.CSS_SELECTOR)


@allure.title("Тест получения трейлера фильма")
@allure.description("Проверяет возможность получения"
                    "трейлера фильма:"
                    "переход по кнопкам и выбор трейлера.")
@allure.feature("Просмотр трейлеров")
@allure.severity(allure.severity_level.NORMAL)
def test_get_trailer_to_buy(driver) -> None:
    """
    Тест получения трейлера.

    Args:
        driver: фикстура.

    Returns:
        None: Тест не возвращает значение, выполняет проверки через assert.
    """
    sh_btn: str = os.getenv("SH_BTN")
    press_f: str = os.getenv("PRESS_F")
    ch_trailer: str = os.getenv("CH_TRAILER")
    button_txt: str = os.getenv("BTN_TXT")
    page = UiPage(driver, base_url)

    with allure.step("Открыть сайт"):
        page.open_site()

    with allure.step("Пройти капчу"):
        page.capcha()

    with allure.step("Выбрать кнопку 'Магазин' слева"):
        page.search_by_css(sh_btn)
        page.click_element(sh_btn, by=By.CSS_SELECTOR)

    with allure.step("Проверить текст на кнопке 'О фильме'"):
        btn_txt = page.search_by_css(button_txt)
        txt_from_btn: str = btn_txt.text
        with allure.step("Ожидаемый текст на кнопке: 'О фильме'"):
            assert txt_from_btn == "О фильме"

    with allure.step("Нажать на фильм"):
        page.search_by_css(press_f)
        page.click_element(press_f, by=By.CSS_SELECTOR)

    with allure.step("Выбрать кнопку 'Трейлер'"):
        page.search_by_css(ch_trailer)
        page.click_element(ch_trailer, by=By.CSS_SELECTOR)


@allure.title("Тест получения топ 250 сериалов")
@allure.description("Проверяет возможность получения"
                    "топ 250 сериалов: переход по кнопкам"
                    "и проверку текста на странице.")
@allure.feature("Сериалы")
@allure.severity(allure.severity_level.NORMAL)
def test_get_top_soap(driver) -> None:
    """
    Тест получения топа сериалов.

    Args:
        driver: фикстура.

    Returns:
        None: Тест не возвращает значение,
        выполняет проверки через assert.
    """
    soap_btn: str = os.getenv("SOAP_BTN")
    best_soap: str = os.getenv("BEST_SOAP")
    choose_online: str = os.getenv("COOSE_ONLINE")
    txt_best_ser: str = os.getenv("TXT_BEST_SER")
    page: UiPage = UiPage(driver, base_url)

    with allure.step("Открыть сайт"):
        page.open_site()

    with allure.step("Пройти капчу"):
        page.capcha()

    with allure.step("Нажать на кнопку 'Сериалы'"):
        page.search_by_xpath(soap_btn)
        page.click_element(soap_btn, by=By.XPATH)

    with allure.step("Выбрать кнопку 'Сериал слева'"):
        page.search_by_xpath(best_soap)
        page.click_element(best_soap, by=By.XPATH)

    with allure.step("Нажать на '250 лучших сериалов'"):
        page.search_by_xpath(choose_online)
        page.click_element(choose_online, by=By.XPATH)

    with allure.step("Найти элемент с текстом '250 лучших сериалов'"):
        text_ser = page.search_by_css(txt_best_ser)
        text_serial: str = text_ser.text

    with allure.step("Проверить,"
                     "что текст элемента равен '250 лучших сериалов'"):
        assert text_serial == "250 лучших сериалов"


@allure.title("Негативный тест поиска"
              "(проверка сообщения об ошибке)")
@allure.description("Проверяет отображение"
                    "сообщения об ошибке при неудачном поиске.")
@allure.feature("Поиск")
@allure.severity(allure.severity_level.CRITICAL)
def test_neg_test_search(driver) -> None:
    """
    Негативный тест (проверка сообщения об ошибке).
    """
    film_name: str = os.getenv("F_NAME")
    input_film_name: str = os.getenv("INPUT_NAME")
    error_element: str = os.getenv("ERROR_ELEMENT")
    btn_enter: str = os.getenv("BTN_ENTER")
    page: UiPage = UiPage(driver, base_url)

    with allure.step("Открыть сайт"):
        page.open_site()
    with allure.step("Пройти капчу"):
        page.capcha()

    with allure.step(
            "Ввести в поле поиска название не существующего фильма "):
        page.input_txt(film_name, input_film_name, by=By.CSS_SELECTOR)

    with allure.step("Нажать кнопку поиска"):
        page.search_by_css(btn_enter)
        page.click_element(btn_enter, by=By.CSS_SELECTOR)

    with allure.step("Получить элемент с сообщением об ошибке"):
        error_message_element = page.search_by_css(error_element)
        error_message_text: str = error_message_element.text

    with ((allure.step("Проверить сообщение об ошибке."))):
        assert ("К сожалению, по вашему запросу ничего не найдено..."
                )in error_message_text


@allure.title("Тест поиска актёра")
@allure.description("Проверяет корректность"
                    "результатов поиска актёра по имени.")
@allure.feature("Поиск")
@allure.severity(allure.severity_level.NORMAL)
def test_search_actor(driver) -> None:
    """
    Тест поиска актёра.
    """
    actor_name: str = os.getenv("ACTOR_NAME")
    input_name: str = os.getenv("INPUT_NAME")
    btn_enter: str = os.getenv("BTN_ENTER")
    element: str = os.getenv("ELEMENT")
    page: UiPage = UiPage(driver, base_url)

    with allure.step("Открыть сайт"):
        page.open_site()
    with allure.step("Пройти капчу"):
        page.capcha()

    with allure.step("Ввести в поле поиска имя актёра"):
        page.input_txt(actor_name, input_name, by=By.CSS_SELECTOR)

    with allure.step("Нажать кнопку поиска"):
        page.search_by_css(btn_enter)
        page.click_element(btn_enter, by=By.CSS_SELECTOR)

    with allure.step("Получить элемент с результатами поиска"):
        message = page.search_by_css(element)
        name_check: str = message.text

    with allure.step("Проверить, что в результатах"
                     "поиска есть 'Константин Хабенский'"):
        assert "Константин Хабенский" in name_check

    with allure.step("Проверить, что в результатах "
                     "поиска есть введённое имя актёра"):
        assert actor_name in name_check
