# a= "myname"
# b= "Akhilesh mishra"

# # f string
# # print(f' {str.upper(a)} is  _>>> {b} ')


# print( " Myname is  _>>> Akhilesh mihsra")

# api call to github to pull all repossitiries.

import requests

github_user = "akhileshmishrabiz"
url = f"https://api.github.com/users/{github_user}/repos"

response = requests.get(url).json()
# print(response)

for item in response:
    # print(item.get("name"))
    print(f'https://github.com/{item.get("full_name")}')

# https://github.com/akhileshmishrabiz/Devops-zero-to-hero

# <Response [200]> -> success
# <Response [404]> -> not found
