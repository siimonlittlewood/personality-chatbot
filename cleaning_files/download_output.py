import urllib.request
import base64
import os

# 1. Enter your credentials directly
username = "simonjayl"
api_key = "KGAT_238a186fdcdfc62d7501a7a052ae25d8"  # <-- Put your Kaggle API key here

# 2. Target your specific notebook and version
owner = "simonjayl"
kernel = "notebooke6d124d088"
version = 2

# This is the raw API endpoint, which properly accepts API tokens for private notebooks
url = f"https://www.kaggle.com/api/v1/kernels/output/download/{owner}/{kernel}?versionNumber={version}"

# 3. Build browser headers to sneak past the firewall and authenticate
auth_str = f"{username}:{api_key}"
auth_b64 = base64.b64encode(auth_str.encode()).decode()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Authorization": f"Basic {auth_b64}"
}

req = urllib.request.Request(url, headers=headers)
output_filename = f"{kernel}_version_{version}.zip"

print(f"Connecting straight to Kaggle API for Version {version}...")

try:
    with urllib.request.urlopen(req) as response:
        with open(output_filename, 'wb') as out_file:
            out_file.write(response.read())
    print(f"\n🎉 Success! Your Version 2 output file has been saved to:\n{os.path.abspath(output_filename)}")
except Exception as e:
    print(f"\n❌ Download failed: {e}")