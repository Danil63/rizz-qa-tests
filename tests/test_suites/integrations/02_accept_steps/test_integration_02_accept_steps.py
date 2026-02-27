"""integration-02: Принятие шагов интеграции рекламодателем + проверка чата."""
import allure
import pytest
from playwright.sync_api import Page

from tests.pages.integration_page import IntegrationPage

WORKS_URL = "https://app.rizz.market/app/advertiser/works"
EXPECTED_MESSAGE = "Приступаю к выполнению работы"
REPLY_MESSAGE = "Хорошо, мне все понравилось!"


@pytest.mark.regression
@pytest.mark.integrations
@allure.epic("Интеграции рекламодателя")
@allure.feature("Принятие шагов интеграции")
@allure.story("Принять 4 шага, проверить чат, отправить сообщение")
@allure.tag("Regression", "Integrations", "AcceptSteps")
class TestIntegration02AcceptSteps:

    @allure.title(
        "integration-02: works → danil23319 → принять 4 шага → чат → сообщение"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_accept_steps_and_chat(self, advertiser_page: Page):
        page = IntegrationPage(advertiser_page)

        # Переход на страницу интеграций рекламодателя
        page.open_advertiser_works()

        # Шаг 1: клик по нику danil23319
        page.click_blogger_nick_danil()

        # Шаг 2: принять все 4 шага (retry если кнопка не исчезла)
        page.accept_all_steps(max_retries=5)

        # Шаг 3: открыть чат с блогером
        page.open_advertiser_chat()

        # Шаг 4: проверить сообщение блогера
        page.wait_for_chat_message(EXPECTED_MESSAGE)

        # Шаг 5: отправить ответ
        page.send_advertiser_message(REPLY_MESSAGE)

        # Шаг 6: неявное ожидание
        advertiser_page.wait_for_timeout(2_000)

        # Шаг 7: проверить отправленное сообщение
        page.wait_for_chat_message(REPLY_MESSAGE)
