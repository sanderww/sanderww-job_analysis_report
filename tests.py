# Save the summaries as a PDF file
import pdfkit
from datetime import datetime
import os
from template_script import html_base
output_folder = "report_output"
job_title = "product manager"
location = "netherlands"
"""test HTML layout"""

if __name__ == "__main__":

    all_summaries_html = """ul>
    <li><p><strong>Company and Title</strong>: BettingJobs, Product Owner - Sports Trading</p></li>
    <li><p><strong>Technical Skills Required</strong>: </p>

    <ul>
    <li>Experience in a sports trading environment</li>
    <li>Proficient in Agile software development practices</li>
    <li>Strong grasp of technical and functional aspects of Sportsbook Trading platforms (both back-end and front-end)</li>
    <li>Integration of external trading tools and consoles</li>
    <li>Ability to analyze market data, user feedback, and analytics</li>
    </ul></li>"""

    todays_date = datetime.now().strftime("%Y-%m-%d:%H-%M")
    # Get today's date in the desired format
    pdf_file_name = os.path.join(output_folder, f"test_pdf_results_{job_title}_{location}_{todays_date}.pdf")

    full_html = html_base.replace("{all_summaries_html}", all_summaries_html)
    full_html = full_html.replace("{job_title}", job_title)
    full_html = full_html.replace("{location}", location)
    full_html = full_html.replace("{today}", datetime.now().strftime("%d-%m-%Y"))
    print(full_html)
    # Convert HTML to PDF
    pdfkit.from_string(full_html, pdf_file_name)

    print(f"PDF report saved to {pdf_file_name}")


