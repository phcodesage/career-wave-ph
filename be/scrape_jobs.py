from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

def fetch_page(url):
    """Fetches a webpage and returns a BeautifulSoup object, includes delay for respecting robots.txt."""
    print(f"Fetching: {url}")
    response = requests.get(url)
    time.sleep(5)  # Crawl-delay as mentioned in robots.txt
    return BeautifulSoup(response.text, 'html.parser')

def process_page(url):
    jobs = []
    while url:
        soup = fetch_page(url)
        job_posts = soup.find_all('div', class_='jobpost-cat-box')
        if not job_posts:
            print("No job posts found.")
        for job in job_posts:
            # Extract the job URL from the anchor tag
            job_link = job.find('a')['href'] if job.find('a') else None
            job_url = f"https://www.onlinejobs.ph{job_link}" if job_link else "#"
            
            title = job.find('h4').text.strip() if job.find('h4') else "No Title"
            description = job.find('div', class_='desc').text.strip() if job.find('div', class_='desc') else "No Description"
            posted_date = job.find('p', class_='fs-13').text.strip() if job.find('p', class_='fs-13') else "No Date Info"
            job_type_badge = job.find('span', class_='badge')
            job_type = job_type_badge.text.strip() if job_type_badge else "Not specified"
            skills_div = job.find('div', class_='job-tag')
            skills = [skill.text.strip() for skill in skills_div.find_all('a', class_='badge')] if skills_div else []
            
            jobs.append({
                'title': title,
                'description': description,
                'posted_date': posted_date,
                'job_type': job_type,
                'skills': skills,
                'url': job_url
            })

        next_page_link = soup.find('a', string='Next')
        if next_page_link:
            url = 'https://www.onlinejobs.ph' + next_page_link.get('href')
            print(f"Next page link found: {url}")
        else:
            url = None
    return jobs

@app.route('/jobs')
def get_jobs():
    query = request.args.get('query', 'call center')
    start_url = f'https://www.onlinejobs.ph/jobseekers/jobsearch?jobkeyword={query}'
    jobs = process_page(start_url)
    return jsonify(jobs)

@app.route('/jobs/<int:job_id>')
def get_job_details(job_id):
    url = f'https://www.onlinejobs.ph/jobseekers/job/{job_id}'
    soup = fetch_page(url)
    
    # Extract detailed job information
    title = soup.find('h1', class_='job__title').text.strip() if soup.find('h1', class_='job__title') else "No Title"
    description = soup.find('p', id='job-description').text.strip() if soup.find('p', id='job-description') else "No Description"
    
    # Extract job metadata
    work_type = soup.find('p', class_='fs-18').text.strip() if soup.find('p', class_='fs-18') else "Not specified"
    salary = soup.find_all('p', class_='fs-18')[1].text.strip() if len(soup.find_all('p', class_='fs-18')) > 1 else "Not specified"
    hours = soup.find_all('p', class_='fs-18')[2].text.strip() if len(soup.find_all('p', class_='fs-18')) > 2 else "Not specified"
    posted_date = soup.find_all('p', class_='fs-18')[3].text.strip() if len(soup.find_all('p', class_='fs-18')) > 3 else "Not specified"
    
    return jsonify({
        'title': title,
        'description': description,
        'work_type': work_type,
        'salary': salary,
        'hours_per_week': hours,
        'posted_date': posted_date
    })

@app.route('/jobs/<path:job_path>')
def get_job_details_by_path(job_path):
    url = f'https://www.onlinejobs.ph/jobseekers/job/{job_path}'
    soup = fetch_page(url)
    
    title = soup.find('h1', class_='job__title').text.strip() if soup.find('h1', class_='job__title') else "No Title"
    description = soup.find('p', id='job-description').text.strip() if soup.find('p', id='job-description') else "No Description"
    
    # Extract job metadata from the card sections
    job_info = soup.find_all('p', class_='fs-18')
    work_type = job_info[0].text.strip() if len(job_info) > 0 else "Not specified"
    salary = job_info[1].text.strip() if len(job_info) > 1 else "Not specified"
    hours = job_info[2].text.strip() if len(job_info) > 2 else "Not specified"
    posted_date = job_info[3].text.strip() if len(job_info) > 3 else "Not specified"
    
    return jsonify({
        'title': title,
        'description': description,
        'work_type': work_type,
        'salary': salary,
        'hours_per_week': hours,
        'posted_date': posted_date
    })



if __name__ == '__main__':
    app.run(debug=True, port=5000)
