import requests
from bs4 import BeautifulSoup
import pandas as pd
import certifi

def get_project_links():
    url = "https://hprera.nic.in/PublicDashboard"
    try:
        response = requests.get(url, verify=certifi.where())  # Using certifi for SSL verification
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
        return []

    if response.status_code != 200:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    project_links = []
    table = soup.find('table', {'id': 'projectTable'})
    
    if table is None:
        print("Error: Could not find the table with id 'projectTable'")
        return []

    rows = table.find_all('tr')[1:7]  # Get the first 6 projects
    
    for row in rows:
        link = row.find('a', href=True)['href']
        project_links.append("https://hprera.nic.in/PublicDashboard" + link)
    
    return project_links

def get_project_details(url):
    try:
        response = requests.get(url, verify=certifi.where())  # Using certifi for SSL verification
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
        return {}

    if response.status_code != 200:
        print(f"Failed to retrieve project details, status code: {response.status_code}")
        return {}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    details = {}
    
    details['URL'] = url
    
    # Extract GSTIN No
    gstin = soup.find('td', text='GSTIN No').find_next_sibling('td').text.strip()
    details['GSTIN No'] = gstin
    
    # Extract PAN No
    pan = soup.find('td', text='PAN No').find_next_sibling('td').text.strip()
    details['PAN No'] = pan
    
    # Extract Name
    name = soup.find('td', text='Name').find_next_sibling('td').text.strip()
    details['Name'] = name
    
    # Extract Permanent Address
    address = soup.find('td', text='Permanent Address').find_next_sibling('td').text.strip()
    details['Permanent Address'] = address
    
    return details

def main():
    project_links = get_project_links()
    if not project_links:
        print("No project links found.")
        return
    
    projects_data = []
    
    for link in project_links:
        details = get_project_details(link)
        if details:
            projects_data.append(details)
    
    if projects_data:
        df = pd.DataFrame(projects_data)
        df.to_csv('projects_data.csv', index=False)
        print(df)
    else:
        print("No project data found.")

if __name__ == "__main__":
    main()
