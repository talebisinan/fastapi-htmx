from playwright.sync_api import Page, expect
import pytest


@pytest.fixture()
def home_page(page: Page) -> Page:
    page.set_default_timeout(5000)
    page.goto("http://127.0.0.1:8000", timeout=3000, wait_until="load")
    return page


def test_example_is_working(home_page: Page):
    assert home_page.inner_text("h1") == "Organizations"


def test_create_organization(home_page: Page):
    assert home_page.inner_text("#orgs\.counter") == "0"

    home_page.locator('[placeholder="Organization name"]').fill("Henkel")
    home_page.locator('[placeholder="Organization name"]').press("Enter")

    assert home_page.inner_text("#orgs\.counter") == "1"

    home_page.locator('[data-org_delete_name="Henkel"]').click()

    expect(home_page.locator("#orgs\.counter")).to_have_text("0")
