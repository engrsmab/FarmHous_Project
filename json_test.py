import json
import requests
data = requests.get("https://www.googleapis.com/robot/v1/metadata/x509/data-707%40data-305920.iam.gserviceaccount.com")
data =  data.text
data = json.loads(data)
print(data)