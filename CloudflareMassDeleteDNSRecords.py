import requests
import concurrent.futures

def delete_dns_record(api_key, email, zone_id, record_id):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Key': api_key,
        'X-Auth-Email': email,
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print(f"Successfully deleted DNS record with ID {record_id}")
    else:
        print(f"Failed to delete DNS record with ID {record_id}. Status code: {response.status_code}")
        print(response.text)

def delete_all_dns_records(api_key, email, zone_id):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Key': api_key,
        'X-Auth-Email': email,
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200:
        record_ids = [record['id'] for record in data['result']]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda record_id: delete_dns_record(api_key, email, zone_id, record_id), record_ids)
    else:
        print(f"Failed to fetch DNS records. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    api_key = 'API_KEY'
    email = 'EMAIL'
    zone_id = 'ZONE_ID'

    delete_all_dns_records(api_key, email, zone_id)