"""products-05: Переход Товар -> Услуга и архивация выбранной услуги."""

import allure
import pytest

from tests.pages.products_page import ProductsPage


@pytest.mark.regression
@pytest.mark.products
@allure.epic("Продукты рекламодателя")
@allure.feature("Фильтрация и архивация")
@allure.story("Переход Товар/Услуга и архивация через меню")
@allure.tag("Regression", "Products", "Positive")
class TestProducts05:
    """products-05: Выбрать Услуга, найти карточку while-циклом, архивировать."""

    @allure.title("products-05: Товар -> Услуга -> найти по заголовку -> Архивировать")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_products_05_switch_product_service(self, products_page: ProductsPage):
        # 1) Старт на странице продуктов
        products_page.expect_loaded()
        products_page.accept_cookies()

        # 2) Dropdown "Товар" -> выбрать "Услуга"
        products_page.select_product_type("Услуга")

        # 3) Выбрать target-услугу (берём первую в отфильтрованном списке)
        total_services = products_page.product_titles.count()
        assert total_services > 0, "Список услуг пуст после фильтрации"
        target_title = (products_page.product_titles.first.get_attribute("alt") or "").strip()
        assert target_title, "Не удалось получить заголовок услуги из карточки"

        # 4) Циклом while пройти заголовки и найти нужный
        found_index = products_page.find_service_index_by_title_while(target_title)

        allure.attach(
            f"Найденная услуга: {target_title}\nИндекс: {found_index}",
            name="Выбранная услуга для архивации",
            attachment_type=allure.attachment_type.TEXT,
        )

        # 5) Нажать троеточие и выбрать "Архивировать"
        products_page.archive_service_by_index(found_index)

        # 6) Явная пауза 3 секунды после архивации
        products_page.page.wait_for_timeout(3000)
