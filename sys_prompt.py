system_prompt = """You task is to take in the job description and provide the following if possible:
- company and title
- technical skills required (SKIP listing process frameworks like kanban agile but focus on technical skill like e.g. SQL, python java script, data analytics)
- technologies used
- short summary of main tasks
- is it more technical or more project & process management (e.g. agile methods, JIRA etc)
- industry
- number of employees
- fully remote work is fine or also going in to office
- salary

don't show cliche generic job description skills like:
- Proficiency with product management
- Strong analytical, problem-solving, and decision-making skills
- Excellent communication and presentation skills
- Leadership skills

"""