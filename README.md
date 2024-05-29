# Medicare CPT Code Scraper and Redshift Updater
This script automates the process of scraping Medicare reimbursement data for specific CPT codes and updating a Redshift database table with the retrieved information.

## Functionality

Redshift Connection: Establishes a connection to a Redshift database using provided credentials.

CPT Code Retrieval: Fetches a list of unique CPT codes from a table named "cpt_codes" in the Redshift database.

## Medicare Website Scraping:

Opens a Chrome browser instance using Selenium WebDriver.

Navigates to the Medicare Procedure Price Lookup tool.

Iterates through a subset of the CPT codes.

## For each code:

Enters the code into the search bar.

Selects the appropriate result.

Clicks to view both Ambulatory Surgical Center (ASC) and Hospital details.

Scrapes the following data points for both ASC and Hospital settings:

Total Cost

Doctor Fee

Facility Fee

Medicare Payment

Patient Pay

## Data Storage: 

Stores the scraped data in a list of dictionaries.

## Redshift Update:

Constructs and executes SQL UPDATE statements to update the corresponding rows in the "cpt_codes" table with the scraped data.

Commits the changes to the database.

## Browser Closure: 

Closes the Chrome browser instance.

## Requirements

## Libraries:

redshift_connector: For connecting to the Redshift database.

pandas: For data manipulation and DataFrame creation.

selenium: For web browser automation.

csv: For potential CSV file handling (not used in the current script).

numpy: For potential numerical operations (not used in the current script).

ChromeDriver: Ensure you have ChromeDriver installed and its path correctly specified in the DRIVER_PATH variable.

Redshift Credentials: Replace the placeholders in the connect function with your actual Redshift database credentials.

CPT Codes Table: The script assumes the existence of a table named "cpt_codes" in your Redshift database with a column named "cpt_code" to store the CPT codes.

## Usage

Install the required libraries using pip install.

Update the DRIVER_PATH and Redshift credentials.

Run the script. It will scrape the data for the specified CPT codes and update your Redshift database.

### Disclaimer:

Web scraping is subject to the terms and conditions of the target website. Use this script responsibly and ensure compliance with any applicable regulations.
