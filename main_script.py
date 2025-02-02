import warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

job_title = "head of product"
location = "South Africa"
max_jobs = 5
output_folder = "report_output"
linkedin_url = "https://www.linkedin.com/login"
linkedin_jobs_url = "https://www.linkedin.com/jobs/"
remote_filter = True
senior_filter = True

from dotenv import load_dotenv
import os
import time
import random
import markdown2
import pdfkit
from datetime import datetime
import keyring  # store credentials in mac key store
import getpass  # for secure password input

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils import get_llm_analysis, setup_credentials
from sys_prompt import system_prompt,system_prompt_find_great_job, system_prompt_find_worst_job
from template_script import html_base

# First time setup (run once to store credentials):
try:
    username = keyring.get_password("linkedin", "username")
    password = keyring.get_password("linkedin", username)
    if not username or not password:
        raise keyring.errors.KeyringError
except keyring.errors.KeyringError:
    print("Credentials not found. Running first-time setup...")
    setup_credentials()
    username = keyring.get_password("linkedin", "username")
    password = keyring.get_password("linkedin", username)

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print("\nOpening LinkedIn login page...")
driver.get(linkedin_url)

print("Entering login credentials...")
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.XPATH, "//button[@type='submit']").click()

input("\n\n\nPress Enter after login successfull...\n\n")
# Wait for the feed page to load
wait = WebDriverWait(driver, 10)
feed_page = wait.until(EC.url_contains("https://www.linkedin.com/feed/"))

print(f"Navigating to LinkedIn Jobs page: {linkedin_jobs_url}...")

driver.get(linkedin_jobs_url)

# Wait for the jobs page to load
jobs_page = wait.until(EC.url_contains(linkedin_jobs_url))

print(f"Entering job search term: '{job_title}'")
search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-box__text-input")))
search_input.send_keys(job_title)

print("Submitting search...")
search_input.send_keys(Keys.RETURN)
time.sleep(3)


# LinkedIn URL filters
print(f"Applying filters for remote work = {remote_filter} and experience level = {senior_filter}...")

filters = ""
if remote_filter:
    filters += "&f_WT=2"
if senior_filter:
    filters += "&f_E=4%2C5%2C6"

driver.get(driver.current_url + filters)
time.sleep(2)

print(f"Setting location filter to: '{location}'")
location_input = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//input[@aria-label='City, state, or zip code' and not(@disabled)]")
    )
)
time.sleep(2)
location_input.clear()
location_input.send_keys(location)
time.sleep(2)

print("Clicking search button to apply filters...")
search_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.jobs-search-box__submit-button")
    )
)
search_button.click()
time.sleep(5)

# Initialize a list to store job IDs
job_ids = []

# Scroll to load more jobs (if necessary)
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new jobs to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Exit loop if no more jobs are loaded
    last_height = new_height

# Find all elements with the 'data-occludable-job-id' attribute
elements = driver.find_elements(By.CSS_SELECTOR, '[data-occludable-job-id]')

# Extract the job IDs from each element
for element in elements:
    job_id = element.get_attribute("data-occludable-job-id")
    if job_id:
        job_ids.append(job_id)

# Print the list of job IDs
print(f"{len(job_ids)} JOBS FOUND, job ids:")
print(job_ids)

if len(job_ids) > max_jobs:
    job_ids = job_ids[:max_jobs]

# Iterate over each job ID and scrape content
all_summaries_html = ""
for count, job_id in enumerate(job_ids):
    print(f"count {count+1} - jobid {job_id}")
    try:
        url = f"https://www.linkedin.com/jobs/search/?currentJobId={job_id}"
        
        print(f"checking url: {url}")

        driver.get(url)
        # Retry mechanism for waiting for the job details element to load
        max_retries = 3  # Number of attempts
        for attempt in range(max_retries):
            try:
                #job_details_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".job-view-layout.jobs-details")))
                job_details_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".job-view-layout")))
                time.sleep(random.uniform(6, 10))
                break  # Exit the loop if successful
            except Exception as e:
                print(f"Attempt {attempt + 1} failed")
                time.sleep(5)  # Wait for 5 seconds before retrying
        else:
            # If we exhaust all attempts, handle the exception
            print(f"Failed to find job details element after {max_retries} attempts.")
            continue  # or raise an exception, or handle it as needed
        
        # Extract the text from the job details element and its children
        job_details_text = job_details_element.text
        print(f"JOB {job_id}:\n")
        summarise_text= get_llm_analysis(content=job_details_text,system_prompt=system_prompt)
        print("\n\n\nSUMMARISED:")
        
        
        summarise_text_markdown = markdown2.markdown(summarise_text)
        print(summarise_text_markdown)

        summarise_text_markdown_full= f"""
            <div class="job-summary">
            <h3>JOB ID: {job_id}</h3>
            <p><strong>URL:</strong> <a href="{url}">{url}</a></p>
            <div class="job-description">
                {summarise_text_markdown}
            </div>
            </div>"""
        # Add the current summary to the all_summaries_markdown variable
        all_summaries_html += summarise_text_markdown_full + "\n\n"  # Add a newline for separation

        # Add a random delay
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Error processing job ID {job_id}: {e}")
        continue


# Close the browser
driver.quit()

# Save the summaries as a PDF file
todays_date = datetime.now().strftime("%Y-%m-%d:%H-%M")
# Get today's date in the desired format
pdf_file_name = os.path.join(output_folder, f"results_{job_title}_{location}_{todays_date}.pdf")

full_html = html_base.replace("{all_summaries_html}", all_summaries_html)
full_html = full_html.replace("{job_title}", job_title)
full_html = full_html.replace("{location}", location)
full_html = full_html.replace("{today}", datetime.now().strftime("%d-%m-%Y"))
print(full_html)
# Convert HTML to PDF
pdfkit.from_string(full_html, pdf_file_name)
print(f"PDF report saved to {pdf_file_name}")


print("\nWORST JOB MATCHES\n")
best_jobs = get_llm_analysis(system_prompt=system_prompt_find_worst_job, content=all_summaries_html)
print(best_jobs)

print("\nBEST JOB MATCHES\n")
worst_jobs = get_llm_analysis(system_prompt=system_prompt_find_great_job, content=all_summaries_html)
print(worst_jobs)
