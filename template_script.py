html_base = """<html>
  <head>
    <meta charset="utf-8" />
    <title>{job_title} - {location} - {today}</title>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
      body {
        font-family: Georgia, serif;
        background-color: #fffaf0;
        color: #5d4037;
        margin: 0;
        padding: 20px;
      }
      .job-summary {
        max-width: 800px;
        margin: 20px auto;
        padding: 20px;
        background-color: #fff8e1;
        border: 1px solid #f0c27b;
        border-radius: 8px;
        box-sizing: border-box;
        page-break-inside: avoid;
      }
      .job-summary h3 {
        margin-top: 0;
        font-size: 1.8em;
      }
      .job-summary p {
        margin: 10px 0;
        line-height: 1.6;
        font-family: 'Open Sans', sans-serif;
      }
      .job-summary a {
        color: #d84315;
        text-decoration: none;
      }
      .job-summary a:hover {
        text-decoration: underline;
      }
      .job-description {
        word-wrap: break-word;
      }
    </style>
  </head>
  <body>
  <h1>Jobs: {job_title} - {location} - {today}</h1>
    <!-- Your accumulated job summaries -->
    {all_summaries_html}
  </body>
</html>
"""
