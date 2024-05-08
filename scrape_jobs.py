import requests
from bs4 import BeautifulSoup
import time

def fetch_page(url):
    """Fetches a webpage and returns a BeautifulSoup object, includes delay for respecting robots.txt."""
    print(f"Fetching: {url}")
    response = requests.get(url)
    time.sleep(5)  # Crawl-delay as mentioned in robots.txt
    return BeautifulSoup(response.text, 'html.parser')

def process_page(soup):
    """Processes each page, extracts job details and finds link to the next page."""
    job_posts = soup.find_all('div', class_='jobpost-cat-box')  # Adjusted to correct class
    if not job_posts:
        print("No job posts found.")
    for job in job_posts:
        title = job.find('h4').text.strip() if job.find('h4') else "No Title"
        description = job.find('div', class_='desc').text.strip() if job.find('div', class_='desc') else "No Description"
        posted_date = job.find('p', class_='fs-13').text.strip() if job.find('p', class_='fs-13') else "No Date Info"
        print(f"Job Title: {title}")
        print(f"Description: {description}")
        print(f"Posted Date: {posted_date}\n")

    next_page_link = soup.find('a', string='Next')  # Assumes pagination control is present
    if next_page_link:
        next_page_url = 'https://www.onlinejobs.ph' + next_page_link.get('href')
        print(f"Next page link found: {next_page_url}")
        next_soup = fetch_page(next_page_url)
        process_page(next_soup)
    else:
        print("No more pages.")

# Starting URL
start_url = 'https://www.onlinejobs.ph/jobseekers/jobsearch?jobkeyword=call+center'
initial_soup = fetch_page(start_url)
process_page(initial_soup)
