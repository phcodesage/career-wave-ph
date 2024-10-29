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
    """Fetches and processes a webpage, extracts job details, handles pagination."""
    jobs = []
    while url:
        soup = fetch_page(url)
        job_posts = soup.find_all('div', class_='jobpost-cat-box')
        if not job_posts:
            print("No job posts found.")
        for job in job_posts:
            title = job.find('h4').text.strip() if job.find('h4') else "No Title"
            description = job.find('div', class_='desc').text.strip() if job.find('div', class_='desc') else "No Description"
            posted_date = job.find('p', class_='fs-13').text.strip() if job.find('p', class_='fs-13') else "No Date Info"
            
            # Extract job type badge
            job_type_badge = job.find('span', class_='badge')
            job_type = job_type_badge.text.strip() if job_type_badge else "Not specified"
            
            # Extract skills
            skills_div = job.find('div', class_='job-tag')
            skills = [skill.text.strip() for skill in skills_div.find_all('a', class_='badge')] if skills_div else []
            
            jobs.append({
                'title': title,
                'description': description,
                'posted_date': posted_date,
                'job_type': job_type,
                'skills': skills
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
