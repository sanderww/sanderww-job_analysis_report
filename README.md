# LinkedIn Job Analyzer

  

An automated tool that scrapes LinkedIn job postings and provides AI-powered analysis of job descriptions. The project includes both a command-line scraper and a web interface for analyzing job descriptions.

## To do
add location to script
change into proper structure
add tests  

## commit changes
git add .
git commit -m "update"
git push

## Features

  

- LinkedIn job search automation

- Remote job filtering

- Experience level filtering

- AI-powered job description analysis

- Web interface for manual job analysis

- PDF report generation

- Configurable system prompts

  

## Project Structure

  

## Prerequisites

  

- Python 3.8+

- Chrome browser

- wkhtmltopdf (for PDF generation)

  

## Installation

  

1. Clone the repository:

  

3. Install wkhtmltopdf:

- Windows: Download from [wkhtmltopdf downloads](https://wkhtmltopdf.org/downloads.html)

- Mac: `brew install wkhtmltopdf`

- Linux: `sudo apt-get install wkhtmltopdf`

  

4. Create a `.env` file with your credentials:

  

## Usage

  

### Command-line Scraper

  

Run the LinkedIn scraper:

  

The scraper will:

1. Log into LinkedIn (requires manual CAPTCHA verification)

2. Search for specified job titles

3. Filter for remote positions and experience levels

4. Generate a PDF report in the `results` folder

  

### Web Interface

  

Start the web interface:

  

Access the web interface at `http://localhost:5000` to:

- Input job descriptions manually

- Configure analysis prompts

- Get instant AI analysis

  

## Configuration

  

- Modify `config/system_prompt.py` to customize the AI analysis

- Adjust search parameters in `src/scraper/linkedin_scraper.py`:

- `search_keys`: Job title to search for

- `location`: Geographic location filter

- Number of jobs to analyze