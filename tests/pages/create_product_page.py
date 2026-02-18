"""POM: Страница создания продукта рекламодателя."""
import allure
from pathlib import Path
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class CreateProductPage(BasePage):
    """Page Object для https://app.rizz.market/app/advertiser/products/create."""

    URL = "https://app.rizz.market/app/advertiser/products/create"

    # Путь к тестовой картинке по умолчанию
    DEFAULT_IMAGE = Path(__file__).parent.parent / "test_data" / "product_image.jpg"

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Хлебные крошки ────────────────────────────────────
        self.breadcrumb = page.get_by_role("navigation", name="breadcrumb")
        self.breadcrumb_products = self.breadcrumb.get_by_role("link", name="Продукты")
        self.breadcrumb_create = self.breadcrumb.get_by_role("link", name="Создание")

        # ── Заголовок и описание ──────────────────────────────
        self.heading = page.get_by_role("heading", name="Создание продукта")
        self.description = page.get_by_text("Заполните поля формы и нажмите «Создать».")

        # ── Загрузка изображения ──────────────────────────────
        self.upload_area = page.get_by_text("Перетащите изображение для загрузки или нажмите")
        self.upload_button = page.get_by_role(
            "button",
            name="Перетащите изображение для загрузки"
        )
        self.file_input = page.locator("input[type='file'][accept='image/jpeg,image/png']")

        # ── Тип задания (табы) ────────────────────────────────
        self.tab_product = page.get_by_role("tab", name="Товар")
        self.tab_service = page.get_by_role("tab", name="Услуга")

        # ── Поля формы ────────────────────────────────────────
        self.input_article = page.get_by_role("textbox", name="Артикул")
        self.input_name = page.get_by_role("textbox", name="Название")
        self.input_description = page.get_by_role("textbox", name="Описание")
        self.input_brand = page.get_by_role("textbox", name="Бренд")
        self.input_price = page.get_by_role("textbox", name="Цена")
        self.input_product_link = page.get_by_role("textbox", name="Ссылка на товар")

        # ── Dropdown'ы (combobox) ─────────────────────────────
        self.select_category = page.get_by_role("combobox", name="Категория")
        self.select_marketplace = page.get_by_role("combobox", name="Маркетплейс")

        # ── Кнопка создания ───────────────────────────────────
        self.submit_button = page.get_by_role("button", name="Создать")

        # ── Cookie-диалог ─────────────────────────────────────
        self.cookie_accept = page.get_by_role("button", name="Принять cookie")

    # ── Методы действий ───────────────────────────────────────

    @allure.step("Принять cookie")
    def accept_cookies(self) -> None:
        """Принять cookie, если диалог отображается."""
        if self.cookie_accept.is_visible(timeout=3000):
            self.cookie_accept.click()

    @allure.step("Загрузка изображения продукта")
    def upload_image(self, file_path: str | Path | None = None) -> None:
        """Загрузить изображение через скрытый input[type=file]."""
        path = str(file_path or self.DEFAULT_IMAGE)
        self.file_input.set_input_files(path)

    @allure.step('Выбор типа задания: "{task_type}"')
    def select_task_type(self, task_type: str) -> None:
        """Выбрать тип задания: Товар или Услуга."""
        if task_type == "Товар":
            self.tab_product.click()
        elif task_type == "Услуга":
            self.tab_service.click()

    @allure.step('Ввод артикула: "{value}"')
    def fill_article(self, value: str) -> None:
        """Заполнить поле Артикул."""
        self.input_article.fill(value)

    @allure.step('Ввод названия: "{value}"')
    def fill_name(self, value: str) -> None:
        """Заполнить поле Название."""
        self.input_name.fill(value)

    @allure.step('Ввод описания: "{value}"')
    def fill_description(self, value: str) -> None:
        """Заполнить поле Описание."""
        self.input_description.fill(value)

    @allure.step('Ввод бренда: "{value}"')
    def fill_brand(self, value: str) -> None:
        """Заполнить поле Бренд."""
        self.input_brand.fill(value)

    @allure.step('Ввод цены: "{value}"')
    def fill_price(self, value: str) -> None:
        """Заполнить поле Цена."""
        self.input_price.fill(value)

    @allure.step('Ввод ссылки на товар: "{value}"')
    def fill_product_link(self, value: str) -> None:
        """Заполнить поле Ссылка на товар."""
        self.input_product_link.fill(value)

    @allure.step('Выбор категории: "{option}"')
    def select_category_option(self, option: str) -> None:
        """Выбрать категорию из dropdown."""
        self.select_category.click()
        self.page.get_by_role("option", name=option, exact=True).click()

    @allure.step('Выбор маркетплейса: "{option}"')
    def select_marketplace_option(self, option: str) -> None:
        """Выбрать маркетплейс из dropdown."""
        self.select_marketplace.click()
        self.page.get_by_role("option", name=option, exact=True).click()

    @allure.step('Нажатие кнопки "Создать"')
    def click_submit(self) -> None:
        """Нажать кнопку Создать."""
        self.submit_button.click()

    @allure.step("Заполнение всех полей формы")
    def fill_all_fields(
        self,
        article: str,
        name: str,
        description: str,
        category: str,
        brand: str,
        marketplace: str,
        price: str,
        product_link: str,
        task_type: str = "Товар",
        image_path: str | Path | None = None,
    ) -> None:
        """Заполнить все поля формы создания продукта."""
        self.upload_image(image_path)
        self.select_task_type(task_type)
        self.fill_article(article)
        self.fill_name(name)
        self.fill_description(description)
        self.select_category_option(category)
        self.fill_brand(brand)
        self.select_marketplace_option(marketplace)
        self.fill_price(price)
        self.fill_product_link(product_link)

    # ── Методы проверок ───────────────────────────────────────

    @allure.step("Проверка: страница создания продукта загружена")
    def expect_loaded(self) -> None:
        """Проверить что страница создания продукта загружена."""
        self.expect_url_contains(r".*/app/advertiser/products/create")
        expect(self.heading).to_be_visible()

    @allure.step("Проверка: хлебные крошки видны")
    def check_breadcrumb_visible(self) -> None:
        """Проверить видимость хлебных крошек."""
        expect(self.breadcrumb_products).to_be_visible()
        expect(self.breadcrumb_create).to_be_visible()

    @allure.step("Проверка: все поля формы видны")
    def check_form_fields_visible(self) -> None:
        """Проверить видимость всех полей формы."""
        expect(self.upload_area).to_be_visible()
        expect(self.tab_product).to_be_visible()
        expect(self.tab_service).to_be_visible()
        expect(self.input_article).to_be_visible()
        expect(self.input_name).to_be_visible()
        expect(self.input_description).to_be_visible()
        expect(self.select_category).to_be_visible()
        expect(self.input_brand).to_be_visible()
        expect(self.select_marketplace).to_be_visible()
        expect(self.input_price).to_be_visible()
        expect(self.input_product_link).to_be_visible()
        expect(self.submit_button).to_be_visible()

    @allure.step("Проверка: таб Товар выбран по умолчанию")
    def check_product_tab_selected(self) -> None:
        """Проверить что таб Товар выбран по умолчанию."""
        expect(self.tab_product).to_have_attribute("aria-selected", "true")

    @allure.step("Проверка: placeholder цены корректный")
    def check_price_placeholder(self) -> None:
        """Проверить placeholder поля Цена."""
        expect(self.input_price).to_have_attribute("placeholder", "Цена в рублях")
