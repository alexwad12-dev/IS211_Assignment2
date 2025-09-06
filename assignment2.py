#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IS211 Assignment 2 - Python Standard Library
Fork Version with snake_case variables and assignment function names
"""

import argparse
import urllib.request
import logging
import datetime
import csv
import sys


def download_data(url):
    """
    Downloads the data from the given URL.

    Args:
        url (str): The URL to download data from

    Returns:
        str: The content of the downloaded file

    Raises:
        Various urllib.request exceptions if download fails
    """
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def process_data(file_content):
    """
    Processes CSV data and converts it into a dictionary mapping IDs to person info.

    Args:
        file_content (str): Raw CSV content as a string

    Returns:
        dict: Dictionary mapping ID numbers to (name, birthday) tuples
    """
    # Get the logger we'll set up in main()
    logger = logging.getLogger('assignment2')

    # This will store our final data: {ID: (name, birthday_object)}
    person_data = {}

    # Split the CSV data into lines for processing
    csv_lines = file_content.strip().split('\n')

    # Create a CSV reader that treats first line as headers
    csv_reader = csv.DictReader(csv_lines)

    # Keep track of line numbers for error logging
    line_number = 2  # Start at 2 because line 1 is headers

    for row in csv_reader:
        try:
            # Extract data from the CSV row
            person_id = int(row['id'])
            name = row['name']
            birthday_str = row['birthday']

            # Try to convert the birthday string to a datetime object
            # Expected format: dd/mm/yyyy
            try:
                # strptime parses a string into a datetime object
                # %d = day, %m = month, %Y = 4-digit year
                birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y')

                # Store the person's data
                person_data[person_id] = (name, birthday)

            except ValueError:
                # This catches malformed dates like "23/23/2007" or "29/072006"
                logger.error("Error processing line #{} for ID #{}".format(line_number, person_id))

        except (ValueError, KeyError):
            # This catches other parsing errors (like non-integer IDs)
            logger.error("Error processing line #{} - general parsing error".format(line_number))

        # Move to next line number
        line_number += 1

    return person_data


def setup_logging():
    """
    Sets up logging to write errors to a file called 'errors.log'.
    """
    # Get or create a logger with the name 'assignment2'
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)

    # Create a file handler to write to 'errors.log'
    file_handler = logging.FileHandler('errors.log', mode='w')  # 'w' overwrites each run

    # Create a formatter for log messages
    formatter = logging.Formatter('%(message)s')  # Just the message, no timestamps
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)


def display_person(id, person_data):
    """
    Displays information for a person with the given ID.

    Args:
        id (int): The ID number to look up (keeping original parameter name)
        person_data (dict): Dictionary mapping IDs to (name, birthday) tuples (keeping original parameter name)

    """
    # Check if the person exists in our data
    if id in person_data:
        name, birthday = person_data[id]
        # Format the birthday as YYYY MM DD (note: spaces, not dashes in output)
        formatted_date = birthday.strftime('%Y %m %d')
        print("Person #{} is {} with a birthday of {}".format(id, name, formatted_date))
    else:
        print("No user found with that id")


def main():
    """
    Main function that coordinates the entire program.
    Uses argparse to get the URL parameter from command line arguments.
    """
    # Set up argparse to handle command line arguments
    parser = argparse.ArgumentParser(description='Process CSV data from a URL')
    parser.add_argument('--url', help='URL to the datafile', type=str, required=True)

    # Parse the command line arguments
    args = parser.parse_args()

    print(f"Running main with URL = {args.url}...")

    # Set up logging first
    setup_logging()

    # Try to download the data
    try:
        print("Downloading data from {}...".format(args.url))
        csv_data = download_data(args.url)
        print("Download successful!")
    except Exception as e:
        print("Error downloading data: {}".format(str(e)))
        sys.exit(1)  # Exit with error code

    # Process the downloaded data
    print("Processing data...")
    person_data = process_data(csv_data)
    print("Processing complete! {} people loaded.".format(len(person_data)))

    # Interactive user input loop
    print("\nYou can now look up people by their ID number.")
    print("Enter a negative number or 0 to exit.")

    while True:
        try:
            # Get user input
            user_input = input("Enter an ID to lookup: ")
            person_id = int(user_input)

            # Check if user wants to exit
            if person_id <= 0:
                print("Goodbye!")
                break

            # Display the person's information
            # Note: using original parameter names for function call
            display_person(person_id, person_data)

        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    """Main entry point - call main() with no parameters"""
    main()