from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import allure
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementNotInteractableException,
    ElementClickInterceptedException
)
from selenium.webdriver.remote.webelement import WebElement

load_dotenv()


class UiPage:
    """
    Класс для работы с UI‑элементами веб‑страницы через Selenium.
    Предоставляет методы для навигации,
    поиска элементов, взаимодействия с ними и обработки ошибок.
    """

    def __init__(self, driver, url):
        """
        Инициализирует экземпляр класса UiPage.

        :param driver: экземпляр WebDriver
        (например, ChromeDriver) для управления браузером
        :type driver: selenium.webdriver.remote.webdriver.WebDriver
        :param url: URL веб‑страницы для открытия
        :type url: str
        """
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(self.driver, 20, 0.5)

    @allure.step("Открытие веб‑сайта по указанному URL")
    def open_site(self):
        """
        Открывает веб‑сайт по указанному URL.

        :return: None
        """
        self.driver.get(self.url)

    @allure.step("Попытка кликнуть по кнопке капчи")
    def capcha(self):
        """
        Пытается кликнуть по кнопке капчи (если она есть).
        При отсутствии элемента или ошибке — игнорирует исключение.

        :return: None
        """
        try:
            captcha_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".CheckboxCaptcha-Button")))
            captcha_button.click()
        except:
            pass

    @allure.step("Получение текущего URL страницы")
    def get_current_url(self) -> str:
        """
        Получает текущий URL открытой страницы
        с задержкой до и после запроса.

        :return: текущий URL страницы в виде строки
        :rtype: str
        """
        current_url = self.driver.current_url
        return current_url

    @allure.step("Поиск видимого элемента на странице по CSS‑селектору")
    def search_by_css(self, css_selector):
        """
        Ищет видимый элемент на странице по CSS‑селектору.

        :param css_selector: CSS‑селектор для поиска элемента
        :type css_selector: str
        :return: найденный WebElement, видимый на странице
        :rtype: selenium.webdriver.remote.webelement.WebElement
        """
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, css_selector)))

    @allure.step("Поиск элемента на странице по XPath: {xpath}")
    def search_by_xpath(self, xpath):
        """
        Ищет присутствующий на странице элемент по XPath.

        :param xpath: XPath‑выражение для поиска элемента
        :type xpath: str
        :return: найденный WebElement (присутствует в DOM)
        :rtype: selenium.webdriver.remote.webelement.WebElement
        """
        return self.wait.until(
            EC.presence_of_element_located((By.XPATH, xpath)))

    @allure.step("Ввод текста в поле ввода с селектором")
    def input_txt(self, text, selector, by: By = By.CSS_SELECTOR):
        """
        Вводит текст в поле ввода, предварительно очистив его.

        :param text: текст для ввода в элемент
        :type text: str
        :param selector: селектор для поиска элемента (CSS или XPath)
        :type selector: str
        :param by: тип селектора (By.CSS_SELECTOR или By.XPATH),
        по умолчанию — By.CSS_SELECTOR
        :type by: selenium.webdriver.common.by.By
        :return: WebElement, в который был введён текст
        :rtype: selenium.webdriver.remote.webelement.WebElement
        """
        element = self.wait.until(EC.element_to_be_clickable((by, selector)))
        element.clear()
        element.send_keys(text)
        return element

    @allure.step("Клик по элементу с селектором '{selector}' (тип: {by})")
    def click_element(
            self,
            selector: str,
            max_attempts: int = 3,
            by: By = By.XPATH
    ) -> WebElement:
        """
        Надёжно кликает по элементу с повторными попытками при ошибках.

        :param selector: Селектор для поиска элемента (XPath или CSS)
        :param max_attempts: максимальное количество попыток
        :param by: тип селектора (By.XPATH или By.CSS_SELECTOR)
        :return: WebElement при успешном клике
        :raises: Исключение, если все попытки провалились
        """

        for attempt in range(1, max_attempts + 1):
            with allure.step(
                    f"Попытка {attempt}/{max_attempts} клика по элементу"):
                try:
                    with allure.step(
                            "Поиск и ожидание кликабельности элемента"):
                        element = self.wait.until(
                            EC.element_to_be_clickable((by, selector)))

                    with allure.step("Прокрутка к элементу (центрирование)"):
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});",
                            element
                        )

                    with allure.step("Основной клик через JavaScript"):
                        self.driver.execute_script(
                            "arguments[0].click();", element)
                    return element  # Возвращаем элемент при успехе

                except StaleElementReferenceException:
                    if attempt == max_attempts:
                        with allure.step(
                                "Исчерпаны все попытки — пробрасываем "
                                "StaleElementReferenceException"):
                            raise
                    with allure.step("Элемент устарел — повторяем попытку"):
                        continue  # Повторяем попытку

                except (ElementNotInteractableException,
                        ElementClickInterceptedException) as e:
                    if attempt == max_attempts:
                        with allure.step(
                                "Исчерпаны все попытки"
                                "— пробрасываем исключение"):
                            raise e
                    # Попытка альтернативного клика (ActionChains)
                    with allure.step(
                            "Попытка альтернативного клика (ActionChains)"):
                        try:
                            short_wait = WebDriverWait(
                                self.driver, timeout=2, poll_frequency=0.1)

                            with allure.step(
                                    "Повторное ожидание кликабельности"):
                                element = short_wait.until(
                                    EC.element_to_be_clickable((by, selector))
                                )

                            with allure.step(
                                    "Альтернативный клик через ActionChains"):
                                actions = ActionChains(self.driver)
                            actions.move_to_element(
                                element).click().perform()
                            return element
                        except (StaleElementReferenceException,
                                ElementNotInteractableException):

                            with allure.step(
                                    "Элемент недоступен для альтернативного"
                                    "клика — продолжаем следующую попытку"):
                                continue
                        except Exception as unexpected_e:

                            with allure.step(
                                    f"Неожиданная ошибка в альтернативном"
                                    f"клике (попытка"
                                    f"{attempt}): {unexpected_e}"):
                                print(f"Unexpected error in"
                                      f"alternative click ("
                                      f"attempt {attempt}): {unexpected_e}")
                                continue

        # Если все попытки исчерпаны, выбрасываем исключение
        with allure.step(
                f"Не удалось кликнуть по элементу"
                f"'{selector}' после {max_attempts} попыток"):
            raise Exception(f"Failed to click element"
                            f"'{selector}' after {max_attempts} attempts")
