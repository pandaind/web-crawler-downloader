# Web Crawler for Video Downloads

A Python web crawler script designed to explore web pages, find video files, and download them. The script supports customisation HTML tags and attributes for discovering videos and links, and it allows for parallel URL exploration.

## Features

- **Download Videos**: Finds and downloads video files from specified HTML tags and attributes.
- **Explore Links**: Follows links on the page to find more videos, with support for recursive crawling.
- **Parallel Processing**: Uses threading to explore and download in parallel for faster execution.
- **Configurable**: Allows customisation of HTML tags and attributes for video sources and links.

## Prerequisites

- Python 3.6 or higher
- `requests` library
- `beautifulsoup4` library

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/pandaind/web-crawler-downloader.git
   cd web-crawler-downloader
   ```

2. **Install Required Libraries**

   You can install the necessary Python libraries using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

## RUN

   ```bash
   ./run.sh
   ```

## Usage

To run the web crawler script, use the following command:

```bash
python crawler.py [START_URL] [FOLDER_PATH] [KEYWORDS] [--max_depth MAX_DEPTH] [--download_tag TAG:ATTRIBUTE] [--explore_tag TAG:ATTRIBUTE]
```

### Arguments

- `START_URL`: The starting URL for the web crawler.
- `FOLDER_PATH`: The folder path where downloaded videos will be saved.
- `KEYWORDS`: Space-separated keywords to filter links and videos.
- `--max_depth`: (Optional) Maximum depth to crawl. Default is `2`.
- `--download_tag`: (Optional) Tag and attribute used to find video sources (format: `tag:attribute`). Default is `source:src`.
- `--explore_tag`: (Optional) Tag and attribute used to find links to explore (format: `tag:attribute`). Default is `a:href`.

### Example

To start crawling from `https://example.com` and download videos to the `./videos` folder, with a maximum depth of `3` and using default tags and attributes:

```bash
python crawler.py https://example.com ./videos "video" --max_depth 3
```

To specify custom tags and attributes for finding videos and links:

```bash
python crawler.py https://example.com ./videos "video" --max_depth 3 --download_tag "source:src" --explore_tag "a:href"
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License
