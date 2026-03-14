products:
	uv run pytest tests/test_suites/products/test_products_01_create_empty.py
	uv run pytest tests/test_suites/products/test_products_02_create_service.py
	uv run pytest tests/test_suites/products/test_products_03_create_product.py
	uv run pytest tests/test_suites/products/test_products_04_create_product_two.py
	uv run pytest tests/test_suites/products/test_products_05_navigate_to_campaigns.py


campaigns:
	uv run pytest tests/test_suites/campaigns/create/test_campaigns_01_create_empty.py
	uv run pytest tests/test_suites/campaigns/create/test_campaigns_02_create.py
	uv run pytest tests/test_suites/campaigns/create/test_campaigns_03_create.py
	uv run pytest tests/test_suites/campaigns/create/test_campaigns_04_create.py
	uv run pytest tests/test_suites/campaigns/create/test_campaigns_05_management_switch_and_title.py
	uv run pytest tests/test_suites/campaigns/edit/test_edit_barter_comp.py
	uv run pytest tests/test_suites/campaigns/edit/test_edit_fix_comp.py


filters:
	uv run pytest tests/test_suites/filters/test_filters_01_search_input.py
	uv run pytest tests/test_suites/filters/test_filters_02_all_dropdowns.py


responses:
	uv run pytest tests/test_suites/responses/01_send_response/test_responses_01_barter.py
	uv run pytest tests/test_suites/responses/01_send_response/test_responses_02_fix.py
	uv run pytest tests/test_suites/responses/01_send_response/test_responses_03_cpm.py
	uv run pytest tests/test_suites/responses/02_accept_response/test_responses_01_process_blogger_response.py
	uv run pytest tests/test_suites/responses/02_accept_response/test_responses_02_process_blogger_response.py
	uv run pytest tests/test_suites/responses/02_accept_response/test_responses_03_process_blogger_response.py


integrations:
	uv run pytest tests/test_suites/integrations/01_send_media/test_integration_01_execute.py
	uv run pytest tests/test_suites/integrations/01_send_media/test_integration_02_fix.py
	uv run pytest tests/test_suites/integrations/02_accept_steps/test_integration_02_accept_steps.py
	uv run pytest tests/test_suites/integrations/02_accept_steps/test_integration_03_fix_accept_steps.py
	uv run pytest tests/test_suites/integrations/03_send_link/test_integration_03_send_link.py
	uv run pytest tests/test_suites/integrations/03_send_link/test_integration_04_fix_send_link.py
	uv run pytest tests/test_suites/integrations/04_accept_steps/test_integration_04_accept_steps.py
	uv run pytest tests/test_suites/integrations/04_accept_steps/test_integration_05_fix_accept_social_link.py
	uv run pytest tests/test_suites/integrations/06_signing_act/test_integration_06_signing_act.py
	uv run pytest tests/test_suites/integrations/06_signing_act/test_integration_07_fix_signing_act.py



