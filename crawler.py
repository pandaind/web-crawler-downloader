import requests
from bs4 import BeautifulSoup
import os
import argparse
from urllib.parse import urljoin
from threading import Thread, Lock
import queue

# Global queue for URLs to be explored and lock for thread-safe operations
url_queue = queue.Queue()
url_lock = Lock()

# Function to download a video file
def download_video(url, folder_path, downloaded_urls):
    if url in downloaded_urls:
        print(f"Already downloaded: {url}")
        return
    try:
        print(f"Attempting to download: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        file_name = url.split('/')[-1]
        with open(os.path.join(folder_path, file_name), 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        downloaded_urls.add(url)
        print(f"Downloaded {file_name}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")

# Function to check if any keyword is in the URL (case-insensitive)
def contains_keyword(url, keywords):
    url_lower = url.lower()
    return any(keyword.lower() in url_lower for keyword in keywords)

# Function to find video files in specified tags and attributes
def find_videos(page_url, folder_path, visited_urls, keywords, downloaded_urls, depth, max_depth, download_tag, explore_tag):
    if depth > max_depth:
        return
    if page_url in visited_urls:
        return
    visited_urls.add(page_url)

    try:
        print(f"Fetching page: {page_url}")
        response = requests.get(page_url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Print a snippet of HTML content for debugging
        print("HTML Snippet:")
        print(soup.prettify()[:1000])  # Print the first 1000 characters for a quick overview

        # Find video files in specified tags and attributes
        video_found = False
        for tag, attr in download_tag:
            for element in soup.find_all(tag, {attr: True}):
                video_url = element[attr]
                if contains_keyword(video_url, keywords):
                    full_url = urljoin(page_url, video_url)
                    print(f"Found video URL: {full_url}")
                    download_video(full_url, folder_path, downloaded_urls)
                    video_found = True

        # Find video files in iframes
        for iframe in soup.find_all('iframe', src=True):
            iframe_url = iframe['src']
            iframe_url = urljoin(page_url, iframe_url)
            print(f"Found iframe URL: {iframe_url}")
            try:
                iframe_response = requests.get(iframe_url)
                iframe_response.raise_for_status()
                iframe_soup = BeautifulSoup(iframe_response.content, 'html.parser')
                video_found = find_videos_in_iframe(iframe_soup, folder_path, keywords, iframe_url, downloaded_urls, download_tag) or video_found
            except requests.RequestException as e:
                print(f"Error fetching iframe content {iframe_url}: {e}")

        if not video_found:
            print("No videos found on this page.")

        # Recursively follow links on the page with specific keywords
        for tag, attr in explore_tag:
            for link in soup.find_all(tag, {attr: True}):
                link_url = link[attr]
                link_url = urljoin(page_url, link_url)
                if contains_keyword(link_url, keywords):
                    with url_lock:
                        if link_url not in visited_urls:
                            print(f"Adding link to queue: {link_url}")
                            url_queue.put((link_url, depth + 1))

    except requests.RequestException as e:
        print(f"Error fetching {page_url}: {e}")

def find_videos_in_iframe(soup, folder_path, keywords, page_url, downloaded_urls, download_tag):
    video_found = False
    for tag, attr in download_tag:
        for element in soup.find_all(tag, {attr: True}):
            video_url = element[attr]
            if contains_keyword(video_url, keywords):
                full_url = urljoin(page_url, video_url)
                print(f"Found video URL in iframe: {full_url}")
                download_video(full_url, folder_path, downloaded_urls)
                video_found = True
    return video_found

# Worker function for exploring URLs
def explore_urls(start_url, folder_path, keywords, max_depth, download_tag, explore_tag):
    visited_urls = set()
    downloaded_urls = set()

    # Start with the initial URL
    url_queue.put((start_url, 0))

    while not url_queue.empty():
        current_url, current_depth = url_queue.get()
        find_videos(current_url, folder_path, visited_urls, keywords, downloaded_urls, current_depth, max_depth, download_tag, explore_tag)
        url_queue.task_done()

def crawl(start_url, folder_path, keywords, max_depth, download_tag, explore_tag):
    # Create folder path if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create and start worker threads for parallel exploration
    num_threads = 4  # Number of threads for parallel exploration
    threads = []
    for _ in range(num_threads):
        thread = Thread(target=explore_urls, args=(start_url, folder_path, keywords, max_depth, download_tag, explore_tag))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Web crawler to download video files from web pages.')
    parser.add_argument('start_url', type=str, help='The starting URL for the web crawler.')
    parser.add_argument('folder_path', type=str, help='The folder path where videos will be downloaded.')
    parser.add_argument('keywords', type=str, nargs='+', help='Keywords to filter links.')
    parser.add_argument('--max_depth', type=int, default=2, help='Maximum depth to crawl.')
    parser.add_argument('--download_tag', type=str, default='source:src', help='Tag and attribute used to find video sources (format: tag:attribute).')
    parser.add_argument('--explore_tag', type=str, default='a:href', help='Tag and attribute used to find links to explore (format: tag:attribute).')

    args = parser.parse_args()

    # Parse the tag and attribute arguments
    download_tag = [tuple(tag_attr.split(':')) for tag_attr in args.download_tag.split(',')]
    explore_tag = [tuple(tag_attr.split(':')) for tag_attr in args.explore_tag.split(',')]

    crawl(args.start_url, args.folder_path, args.keywords, args.max_depth, download_tag, explore_tag)

