job_title = "product manager"
location = "Netherlands"
max_jobs = 10
output_folder = "report_output"

from dotenv import load_dotenv
import os
dotenv_path = os.path.join(os.path.dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)
username = os.getenv('username') 
password = os.getenv('password') 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import markdown2
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils import get_description_analysis
from sys_prompt import system_prompt
# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print("\nOpening LinkedIn login page...")
driver.get("https://www.linkedin.com/login")

print("Entering login credentials...")
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.XPATH, "//button[@type='submit']").click()

input("\n\n\nPress Enter after login successfull...\n\n")
# Wait for the feed page to load
wait = WebDriverWait(driver, 10)
feed_page = wait.until(EC.url_contains("https://www.linkedin.com/feed/"))

print("Navigating to LinkedIn Jobs page...")
job_url = "https://www.linkedin.com/jobs/"
driver.get(job_url)

# Wait for the jobs page to load
jobs_page = wait.until(EC.url_contains(job_url))

print(f"Entering job search term: '{job_title}'")
search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-box__text-input")))
search_input.send_keys(job_title)

print("Submitting search...")
search_input.send_keys(Keys.RETURN)
time.sleep(5)

print("Applying filters for remote work and experience level...")
driver.get(driver.current_url + "&f_E=4%2C5%2C6&f_WT=2")
time.sleep(2)

print(f"Setting location filter to: '{location}'")
location_input = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//input[@aria-label='City, state, or zip code' and not(@disabled)]")
    )
)

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
        summarise_text= get_description_analysis(content=job_details_text,system_prompt=system_prompt)
        print("\n\n\nSUMMARISED:")
        
        
        summarise_text_markdown = markdown2.markdown(summarise_text)
        print(summarise_text_markdown)

        summarise_text_markdown_full=f"""<pre><code>
        <h3>JOB ID: {job_id}</h3>
        <p><strong>URL</strong>: <a href="{url}">{url}</a></p>
        {summarise_text_markdown}</code></pre>"""
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
import pdfkit
from datetime import datetime

todays_date = datetime.now().strftime("%Y-%m-%d:%H-%M")
# Get today's date in the desired format
pdf_file_name = os.path.join(output_folder, f"results_{todays_date}.pdf")

# Convert HTML to PDF
pdfkit.from_string(all_summaries_html, pdf_file_name)

print(f"PDF report saved to {pdf_file_name}")