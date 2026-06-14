from datetime import datetime, timedelta
from nepali_datetime import date as NepaliDate
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

URL = "https://supremecourt.gov.np/cp/" #### This is the url of supreme court case search page. Make sure to update if it changes in the future.

### Adjust these dates as needed. Format: datetime(year, month, day)
START_DATE = datetime(2026, 2, 13)
END_DATE   = datetime(2026, 3, 1)

### This part converts AD date to BS string format required by the webpage. 

def ad_to_bs_str(ad_date):
    bs = NepaliDate.from_datetime_date(ad_date.date())
    return f"{bs.year:04d}-{bs.month:02d}-{bs.day:02d}"

# -------------------------------
# Browser setup
# -------------------------------
options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

driver.get(URL)
print("Opened site")

# -------------------------------
# Locate and set dropdowns ONCE
# -------------------------------
court_type = wait.until(EC.element_to_be_clickable((By.NAME, "court_type")))
court_id   = wait.until(EC.presence_of_element_located((By.NAME, "court_id")))


### --------Please find the codes for court_type and court_id values from the developer tools on the webpage. You can change these values to select different court types and courts as needed.--------

Select(court_type).select_by_value("D")   ### Here "D" stands for District Courts. You can change this value to select other court types if needed.

wait.until(lambda d: len(Select(court_id).options) > 1)
Select(court_id).select_by_value("70")   ### Here "70" is the value for Kathmandu District Court. You can change this value to select other courts if needed.

# -------------------------------
# Storage for all results
# -------------------------------
all_data = []

current_date = START_DATE

while current_date <= END_DATE:
    bs_date = ad_to_bs_str(current_date)

    # ✅ RE-LOCATE date field every loop (CRITICAL FIX)
    faisala_date = wait.until(EC.presence_of_element_located((By.NAME, "faisala_date")))

    # -------------------------------
    # Set date
    # -------------------------------
    driver.execute_script("""
    arguments[0].value = arguments[1];
    arguments[0].dispatchEvent(new Event('input', {bubbles:true}));
    arguments[0].dispatchEvent(new Event('change', {bubbles:true}));
    """, faisala_date, bs_date)

    print(f"\n👉 Enter CAPTCHA for BS date {bs_date}")
    input("👉 After entering captcha in browser, press ENTER here to submit...")

    # ✅ RE-LOCATE submit button every loop
    submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_btn.click()

    # -------------------------------
    # Try scraping table
    # -------------------------------
    try:
        table = wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
        rows = table.find_elements(By.XPATH, ".//tbody/tr")

        print(f"✅ {len(rows)} rows found for {bs_date}")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = []

            for cell in cells:
                links = cell.find_elements(By.TAG_NAME, "a")
                if links:
                    row_data.append(links[0].get_attribute("href"))
                else:
                    row_data.append(cell.text.strip())

            row_data.insert(0, bs_date)
            all_data.append(row_data)

    except TimeoutException:
        print(f"⚠️ No cases found for BS date {bs_date}")

    input(f"✅ Done for {bs_date}. Press ENTER to move to next date...")
    current_date += timedelta(days=1)

# -------------------------------
# Save CSV
# -------------------------------
with open("cases_full_range.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(all_data)

print("\n✅ ALL DONE")
print("✅ Data saved to cases_full_range.csv")

driver.quit()
