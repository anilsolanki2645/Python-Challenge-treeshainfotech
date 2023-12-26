#!/usr/bin/env python3

import argparse
import requests
import json
import csv

class RestfulClient:
    # Base URL for the JSONPlaceholder API
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, method, endpoint, data=None):
        # Constructor to initialize instance variables
        self.method = method
        self.endpoint = endpoint
        self.data = data
        self.output = None  # Output file, initially set to None

    def send_request(self):
        # Method to send an HTTP request
        url = f"{self.BASE_URL}{self.endpoint}"
        response = None

        if self.method == "get":
            # Send a GET request
            response = requests.get(url)
        elif self.method == "post":
            # Send a POST request with JSON data
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=self.data, headers=headers)

        return response

    def process_response(self, response):
        try:
            # Print HTTP status code
            print(f"HTTP Status Code: {response.status_code}")

            # Raise an HTTPError for bad responses (4XX and 5XX)
            response.raise_for_status()

            if self.method == "get":
                # Process GET response and dump to output
                self.dump_output(response.json())
            elif self.method == "post":
                # Process POST response and dump to output
                self.dump_output(response.json())
                if response.status_code == 201:
                    print("Post request successful.")
                else:
                    print(f"Error: {response.text}")
                    exit(1)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP Error: {http_err}")
            exit(1)

        except Exception as err:
            print(f"Error: {err}")
            exit(1)

    def dump_output(self, data):
        if self.output:
            try:
                if self.output.endswith(".json"):
                    # Write JSON data to a JSON file
                    with open(self.output, "w") as json_file:
                        json.dump(data, json_file, indent=2)
                elif self.output.endswith(".csv"):
                    if isinstance(data, list) and data:
                        # Write list of dictionaries to a CSV file
                        with open(self.output, "w", newline="") as csv_file:
                            writer = csv.writer(csv_file)
                            # Write header
                            writer.writerow(data[0].keys())
                            # Write rows
                            for row in data:
                                writer.writerow(row.values())
                    else:
                        print("Invalid data format for CSV output.")
                else:
                    # Dump JSON data to stdout
                    print(json.dumps(data, indent=2))
            except Exception as err:
                print(f"Error while writing output: {err}")
                exit(1)
        else:
            # Dump JSON data to stdout if no output file specified
            print(json.dumps(data, indent=2))

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Simple command-line REST client")
    parser.add_argument("method", choices=["get", "post"], help="Request method")
    parser.add_argument("endpoint", help="Request endpoint URI fragment")
    parser.add_argument("-d", "--data", help="Data to send with request")
    parser.add_argument("-o", "--output", help="Output to .json or .csv file (default: dump to stdout)")

    args = parser.parse_args()

    # Create an instance of RestfulClient
    client = RestfulClient(args.method, args.endpoint, data=args.data)

    # Set the output file attribute in the client
    if args.output:
        client.output = args.output
    else:
        client.output = None

    # Send the request and process the response
    response = client.send_request()
    client.process_response(response)

if __name__ == "__main__":
    # Entry point of the script
    main()
