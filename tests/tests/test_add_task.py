import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")


@pytest.fixture
def driver():
    """Create and tear down a Chrome driver for each test."""
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # uncomment if you want headless

    service = Service()
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()


def wait_for(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def add_todo(driver, text: str):
    """Helper: add a single todo."""
    new_todo = wait_for(driver, (By.CSS_SELECTOR, "input.new-todo"))
    new_todo.clear()
    new_todo.send_keys(text)
    new_todo.send_keys(Keys.ENTER)


def get_todos(driver):
    """Return list of <li> todo elements."""
    return driver.find_elements(By.CSS_SELECTOR, "ul.todo-list li")


def get_todo_labels(driver):
    """Return list of label texts for all todos."""
    return [li.find_element(By.TAG_NAME, "label").text for li in get_todos(driver)]


def open_app(driver, filter_path: str = "/"):
    driver.get(BASE_URL + filter_path)
    wait_for(driver, (By.CSS_SELECTOR, "input.new-todo"))


# -------------------------
# TESTS
# -------------------------


def test_add_single_todo_is_visible(driver):
    open_app(driver)

    add_todo(driver, "Buy milk")

    labels = get_todo_labels(driver)
    assert "Buy milk" in labels
    assert len(labels) == 1


def test_add_multiple_todos(driver):
    open_app(driver)

    add_todo(driver, "Task 1")
    add_todo(driver, "Task 2")
    add_todo(driver, "Task 3")

    labels = get_todo_labels(driver)
    assert labels == ["Task 1", "Task 2", "Task 3"]


def test_mark_todo_completed_updates_class_and_counter(driver):
    open_app(driver)

    add_todo(driver, "Learn Selenium")
    add_todo(driver, "Write tests")

    todos = get_todos(driver)
    # mark first as completed
    first = todos[0]
    toggle = first.find_element(By.CSS_SELECTOR, "input.toggle")
    toggle.click()

    # Completed todo should have class "completed"
    assert "completed" in first.get_attribute("class")

    # Check items left counter (TodoMVC style)
    counter = driver.find_element(By.CSS_SELECTOR, "span.todo-count strong")
    assert counter.text == "1"


def test_filter_active_shows_only_active_todos(driver):
    open_app(driver)

    add_todo(driver, "Active task")
    add_todo(driver, "Completed task")

    todos = get_todos(driver)
    # complete the second one
    second = todos[1]
    second.find_element(By.CSS_SELECTOR, "input.toggle").click()

    # Click on "Active" filter
    active_filter = driver.find_element(By.LINK_TEXT, "Active")
    active_filter.click()

    # Now only active tasks should be visible
    labels = get_todo_labels(driver)
    assert labels == ["Active task"]


def test_filter_completed_shows_only_completed_todos(driver):
    open_app(driver)

    add_todo(driver, "Active task")
    add_todo(driver, "Completed task")

    todos = get_todos(driver)
    # complete the second one
    todos[1].find_element(By.CSS_SELECTOR, "input.toggle").click()

    # Click on "Completed" filter
    completed_filter = driver.find_element(By.LINK_TEXT, "Completed")
    completed_filter.click()

    labels = get_todo_labels(driver)
    assert labels == ["Completed task"]


def test_clear_completed_removes_completed_items(driver):
    open_app(driver)

    add_todo(driver, "Keep me")
    add_todo(driver, "Remove me")

    todos = get_todos(driver)
    # complete second one
    todos[1].find_element(By.CSS_SELECTOR, "input.toggle").click()

    # Click "Clear completed"
    clear_button = driver.find_element(By.CSS_SELECTOR, "button.clear-completed")
    clear_button.click()

    labels = get_todo_labels(driver)
    assert labels == ["Keep me"]


def test_delete_todo_removes_it_from_list(driver):
    open_app(driver)

    add_todo(driver, "Delete this")
    todos = get_todos(driver)
    assert len(todos) == 1

    # hover not needed in HTML, destroy is always there and wired via button
    destroy_button = todos[0].find_element(By.CSS_SELECTOR, "button.destroy")
    destroy_button.click()

    # Now list should be empty
    assert get_todos(driver) == []