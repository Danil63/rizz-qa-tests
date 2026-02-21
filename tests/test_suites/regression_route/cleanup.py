"""Teardown-операции после каждого regression suite."""


def teardown_after_auth() -> None:
    """После auth-сьюта очистка не требуется."""
    return


def teardown_after_products() -> None:
    """Удалить лишние продукты, оставив 1 продукт для campaigns.

    TODO: Реализовать через UI/API под бизнес-правила проекта.
    """
    return


def teardown_after_campaigns() -> None:
    """Удалить лишние кампании, оставив 1 кампанию для filters.

    TODO: Реализовать через UI/API под бизнес-правила проекта.
    """
    return


def teardown_after_filters() -> None:
    """Финальная очистка после полного прогона регресса.

    TODO: Реализовать полную очистку тестовых данных.
    """
    return
