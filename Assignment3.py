import csv
import sys
import urllib.request
import argparse
import io
import re


def download_data(url):
    """
    Downloads the data from the given URL.

    Args:
        url (str): The URL to download data from

    Returns:
        str: The content of the downloaded file
    """
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def read_csv(weblog_data):
    """
    Processes the CSV file, and returns a list of dictionaries.

    :param weblog_data: str
    :return: count of total rows and total image files [dict]
    """
    records = []
    with io.StringIO(weblog_data) as file:
        reader = csv.reader(file, delimiter=',')
        column_names: list = ['path', 'datetime_accessed', 'browser', 'request', 'size']

        for row in reader:
            record = dict(zip(column_names, row))
            records.append(record)

    return records


def count_images(records):
    """
    Checks for .jpg, .gif, .png files extensions in the given dataset.

    Args: records: list of dictionaries

    :return: count of total image files [int]
    """
    image_extensions: list = ['jpg', 'gif', 'png']
    pattern = r'\.(' + '|'.join(image_extensions) + ')$'
    image_count: int = 0

    for record in records:
        if re.search(pattern, record['path'], re.IGNORECASE):
            image_count += 1

    return image_count

def find_image_percentage(image_count: int, rows_total: int):
    """
    Checks for .jpg, .gif, .png files extensions in the given dataset.

    :return: Percentage of total image files [float].
    """
    percentage: float = (image_count / rows_total) * 100
    return percentage

def find_most_used_browser(records):
    """
    Returns the name of the most used browser in the data set.

    Args: records: list of dictionaries

    :return: "The most popular browser in the data set was [Firefox, Chrome, Internet Explorer or Safari]."
    """

    browser_types: list = ['Firefox', 'Chrome', 'Internet Explorer', 'Safari']
    pattern = r'(' + '|'.join(browser_types) + ')'
    browser_counts: dict = {}

    for browser in browser_types:
        browser_counts[browser] = 0

    for record in records:
        match = re.search(pattern, record['browser'])
        if match:
            found_browser = match.group(1)  # Get the actual browser that was found
            browser_counts[found_browser] += 1  # Increment the correct browser

    most_popular = max(browser_counts, key=browser_counts.get)
    return most_popular


def main():
    """
    Main function that coordinates the entire program.
    Uses argparse to get the URL parameter from command line arguments.
    """
    image_count = 0


    # Pull down csv file from web using argparse
    parser = argparse.ArgumentParser(description='Process CSV data from a URL')
    parser.add_argument('--url', help='URL to the datafile', type=str, required=True)
    args = parser.parse_args()

    print(f"Running main with URL = {args.url}...")

    # Set up logging first
    # setup_logging()

    # Try to download the data
    try:
        print("Downloading data from {}...".format(args.url))
        weblog_data = download_data(args.url)
        print("Download successful!")
    except Exception as e:
        print("Error downloading data: {}".format(str(e)))
        sys.exit(1)  # Exit with error code

    records = read_csv(weblog_data)
    image_count = count_images(records)
    total_rows = len(records)
    image_percentage = find_image_percentage(image_count, total_rows)
    browser_count = find_most_used_browser(records)

    print(f"Found {image_count} images out of {total_rows} total.")
    print(f"Image request account for {image_percentage:.2f}% of all requests in data.")
    print(f"Most used browser was {browser_count}.")


if __name__ == '__main__':
    main()