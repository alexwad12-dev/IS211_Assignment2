#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test version without command-line arguments
Perfect for testing in PyCharm
"""

import urllib.request
import csv
import datetime
import logging
import sys

# Hard-coded URL for testing
TEST_URL = "https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv"


def download_data(url):
    """Downloads data from a given URL and returns the content as a string."""
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def processData(csvData):
    """Processes CSV data and converts it into a dictionary mapping IDs to person info."""
    logger = logging.getLogger('assignment2')
    personData = {}
    csvLines = csvData.strip().split('\n')
    csvReader = csv.DictReader(csvLines)
    lineNumber = 2

    for row in csvReader:
        try:
            personId = int(row['id'])
            name = row['name']
            birthdayStr = row['birthday']

            try:
                birthday = datetime.datetime.strptime(birthdayStr, '%d/%m/%Y')
                personData[personId] = (name, birthday)

            except ValueError:
                logger.error("Error processing line #{} for ID #{}".format(lineNumber, personId))

        except (ValueError, KeyError):
            logger.error("Error processing line #{} - general parsing error".format(lineNumber))

        lineNumber += 1

    return personData


def displayPerson(personId, personData):
    """Displays information for a person with the given ID."""
    if personId in personData:
        name, birthday = personData[personId]
        formattedDate = birthday.strftime('%Y %m %d')
        print("Person #{} is {} with a birthday of {}".format(personId, name, formattedDate))
    else:
        print("No user found with that id")


def setupLogging():
    """Sets up logging to write errors to a file called 'errors.log'."""
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    fileHandler = logging.FileHandler('errors.log', mode='w')
    formatter = logging.Formatter('%(message)s')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)


def main():
    """Main function - simplified for testing."""
    # Set up logging first
    setupLogging()

    # Try to download the data
    try:
        print("Downloading data from {}...".format(TEST_URL))
        csv_data = download_data(TEST_URL)
        print("Download successful!")
    except Exception as e:
        print("Error downloading data: {}".format(str(e)))
        sys.exit(1)

    # Process the downloaded data
    print("Processing data...")
    person_data = processData(csv_data)
    print("Processing complete! {} people loaded.".format(len(person_data)))

    # Show some examples
    print("\nTesting with a few IDs:")
    displayPerson(1, person_data)
    displayPerson(13, person_data)  # This should have a date error
    displayPerson(999, person_data)  # This doesn't exist

    # Interactive user input loop
    print("\nYou can now look up people by their ID number.")
    print("Enter a negative number or 0 to exit.")

    while True:
        try:
            user_input = input("Enter an ID to lookup: ")
            person_id = int(user_input)

            if person_id <= 0:
                print("Goodbye!")
                break

            displayPerson(person_id, person_data)

        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == '__main__':
    main()