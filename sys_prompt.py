system_prompt = """You task is to take in the job description and provide the following if possible:
- company and title
- technical skills required (SKIP listing process frameworks like kanban agile but focus on real technical skill like e.g. SQL, python java script, data analytics)
- technologies used
- short summary of main tasks
- is it more technical or more project & process management (e.g. agile methods, JIRA etc)
- industry
- number of employees
- fully remote work is fine or also going in to office
- salary
- Fintech or AI related

don't show cliche generic job description skills like:
- Proficiency with product management
- Strong analytical, problem-solving, and decision-making skills
- Excellent communication and presentation skills
- Leadership skills

"""


system_prompt_find_great_job = """your task is to look through all the jobs listing below and find the jobs that best match
1. company that is small for in stance 100 people or less
2. has a focus on tech skill, not process skills
3. Fintech or AI related
4. job that feels low on buraucracy and high on responsibilities
5. a senior lead role


Return th best jobs you can find with URL and reason why it fits, like:
jobId: 4133558176
URL: https://www.linkedin.com/jobs/search/?currentJobId=4133558176&geoId=102890719&origin=JOBS_HOME_LOCATION_AUTOCOMPLETE&refresh=true
Reasoning: small company, mentions using python and this is a lead role
"""


system_prompt_find_worst_job = """your task is to look through all the jobs listing below and find the jobs that best match
1. company that big 1000+ people. Feels like a corporate
2. has a focus on process management, project management. Feels like a lot of meetings 
3. job that feels high on buraucracy, red tape and office politics


Return th best jobs you can find with URL and reason why it fits, like:
URL: https://www.linkedin.com/jobs/search/?currentJobId=4133558176&geoId=102890719&origin=JOBS_HOME_LOCATION_AUTOCOMPLETE&refresh=true
Reasoning: big company, a lot of mention of managing stakeholders, communciation etc
"""