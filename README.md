# nepal-court-cases-scrapper
This is a simple scrapper to access court cases from all levels of courts in Nepal. You can customize the date loop and the exact court you are looking for.

### Features
** Custom date ranges: This code supports data scrapping form dynamic date ranges. 
** Semi automated: Designed to allow manual resolution of CAPTCHA. This ensures compliance with the platform's terms of service and ethical data scrapping.
** Target Courts: Designed to target a specific court (name and level). Can be configured as per your requirement
** Output: Creates a structured csv file from the HTML table along with the download links of the case files

### How to target a specific court:
1. Open https://supremecourt.gov.np/cp/ in your browser.
2. Open **Developer Tools** (`F12` or right-click and select *Inspect*).
3. Look at the dropdown menus for court levels and names to find the exact backend string codes.
4. Input those matching codes directly into the script configuration variables.
5. Note: This code uses string values "D" indicating "District Court" for "court_type" and "70" indicating "Kathmandu District Court" for "court_id". You can change this as per your requirement at ------ Select(court_type).select_by_value("YOUR_COURT_TYPE")
    Select(court_id).select_by_value("YOUR_COURT_ID") 

### Dependencies
1. Python 3.0
2. Selenium
3. Nepali-datetime
Note: You can install selenium and nepali-datetime through this command on your terminal
 pip install selenium nepali-datetime
