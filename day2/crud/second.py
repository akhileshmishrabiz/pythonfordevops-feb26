import requests

# https://x.com/search?q=claude&src=typed_query

per_page = 5
page = 2

github_user = "akhileshmishrabiz"

url = (
    f"https://api.github.com/users/{github_user}/repos?per_page={per_page}&page={page}"
)

response = requests.get(url).json()
# print(response)

for item in response:
    # print(item.get("name"))
    print(f'https://github.com/{item.get("full_name")}')

# To get the next page, increment page:

# page = 2  -> url becomes ...&page=2
