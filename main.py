import requests
import argparse
import csv


# Function to make GraphQL API call
def make_graphql_call(application_id, api_key):
    url = 'https://api.newrelic.com/graphql'  # Replace with your GraphQL API endpoint
    headers = {
        'Content-Type': 'application/json',
        'API-Key': api_key
    }
    query = '''
        {
          actor {
            entitySearch(query: "domainId=%s") {
              count
              query
              results {
                entities {
                  entityType
                  name
                  guid
                }
              }
            }
          }
        }
    ''' % application_id

    response = requests.post(url, headers=headers, json={'query': query})
    return response.json()


# Read application IDs from a plain-text file
def read_application_ids(file_path):
    with open(file_path, 'r') as file:
        application_ids = file.read().splitlines()
    return application_ids


# Write results to a CSV file
def write_to_csv(results, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Application ID', 'Name', 'GUID'])
        for result in results:
            writer.writerow(result)


# Main function
def main():
    parser = argparse.ArgumentParser(description='GraphQL API Script')
    parser.add_argument('--api-key', required=True, help='API key for authentication')
    parser.add_argument('--file-path', required=True, help='Path to the plain-text file containing application IDs')
    parser.add_argument('--output-file', required=True, help='Path to the output CSV file')
    args = parser.parse_args()

    application_ids = read_application_ids(args.file_path)
    results = []

    for application_id in application_ids:
        response = make_graphql_call(application_id, args.api_key)
        # Process the response as needed
        data = response.get('data', {}).get('actor', {}).get('entitySearch', {}).get('results', {}).get('entities', [])
        for entity in data:
            name = entity.get('name')
            guid = entity.get('guid')
            results.append([application_id, name, guid])

    write_to_csv(results, args.output_file)
    print(f'Results written to: {args.output_file}')


if __name__ == '__main__':
    main()
