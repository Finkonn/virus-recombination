import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.wrlfmd.org/fmdv-genome/fmd-prototype-strains"

response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')

r_tabs = soup.find('div', class_='r-tabs')

serotypes = {}
for li in r_tabs.find_all('li'):
    a_tag = li.find('a')
    serotype_name = a_tag.text.strip()
    panel_id = a_tag['href'].replace('#', '')
    serotypes[serotype_name] = {'panel_id': panel_id, 'tables': []}

for serotype, details in serotypes.items():
    panel_div = soup.find('div', id=details['panel_id'])
    if panel_div:
        accordion_divs = panel_div.find_all('div', class_='accordion')
        for accordion in accordion_divs:
            topotype_headers = accordion.find_all('h3')
            for header in topotype_headers:
                topotype_name = header.get_text(strip=True)
                next_div = header.find_next('div')
                tables = next_div.find_all('table')
                
                for table in tables:
                    headers = table.find_all('th')
                    column_names = [header.get_text(strip=True) for header in headers]

                    table_data = []
                    rows = table.find_all('tr')
                    for row in rows:
                        cols = row.find_all('td')
                        col_data = [col.get_text(strip=True) for col in cols]
                        if col_data:
                            table_data.append(col_data)
                    
                    details['tables'].append({
                        'topotype': topotype_name,
                        'column_names': column_names,
                        'data': table_data
                    })

# Function to save data to an Excel file
def save_to_excel(serotypes, filename="../serotypes.xlsx"):
    data = []

    for serotype, details in serotypes.items():
        for table in details['tables']:
            topotype = table['topotype']
            for row in table['data']:
                row_dict = {
                    "Serotype": serotype,
                    "Topotype": topotype,
                }

                for col_name, col_value in zip(table['column_names'], row):
                    row_dict[col_name] = col_value
                data.append(row_dict)
    
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

save_to_excel(serotypes)
