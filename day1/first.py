data= """
{
    "project": "DevOps Pipeline",
    "team": "Infrastructure Engineering",
    "tools": ["Docker", "Kubernetes", "Jenkins", "Terraform"],
    "practices": ["CI/CD", "Infrastructure as Code", "Monitoring", "Automation"],
    "cloud_provider": ["AWS", "GCP"],
    "monitoring_tools": ["Prometheus", "Grafana", "elastisearch"],

    "status": "active"
}
"""


import json

# print(type(data))

# get json from string
json_data = json.loads(data)
# print(type(json_data))

# print(json_data.items()) 
# this will convert dict to list of tuples

# for key, value in json_data.items():
#     print("-----------------------------")
#     print(f"{key} {value}")



# Give me the monitoring tools used in the project
# keyword monitoring_tools

keyword = "monitoring_tool"
# output = json_data["monitoring_tool"]
# output = json_data.get("monitoring_tool", "No monitoring_tools  key is found in data, are you using the right keyword")
# output = json_data.get(keyword, "No monitoring_tools  key is found in data, are you using the right keyword")

# print(output)

def nice():
    print("Nice!")

def not_nice():
    print("Not nice!")
# if keyword exist, then say nice, else say not nice

# if keyword in json_data:
#     nice()
# else:    not_nice()

if json_data.get(keyword, None):
    nice()
else:    
    not_nice()