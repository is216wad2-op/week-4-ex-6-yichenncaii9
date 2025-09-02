import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = 'file://' + os.path.abspath('ex6.html')  # update as needed
driver.get(url)
time.sleep(1)

select_elem = driver.find_element(By.ID, 'select_item')
select = Select(select_elem)
ul = driver.find_element(By.ID, 'shopList')

added_items = set()

for option in select.options:
    # Select the option
    select.select_by_visible_text(option.text)

    # Dispatch the change event manually (if needed)
    driver.execute_script("""
        var select = arguments[0];
        var event = new Event('change', { bubbles: true });
        select.dispatchEvent(event);
    """, select_elem)

    time.sleep(0.5)

    # Collect current items in the shopping cart
    li_items = ul.find_elements(By.TAG_NAME, 'li')
    current_items = [li.text for li in li_items]

    # The newly added item should be the option's value if not duplicate
    new_item = option.get_attribute('value')
    if new_item not in added_items:
        assert new_item in current_items, f"Expected new item '{new_item}' to be in list."
        added_items.add(new_item)
    else:
        # No duplicates allowed; count of new_item in list should not increase
        count = current_items.count(new_item)
        assert count == 1, f"Duplicate '{new_item}' found in shopping cart."

print("All tests passed!")

driver.quit()
