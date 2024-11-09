import io
import os
import json
import httpx
import zipfile
from datetime import datetime, timezone
import shutil

def timeAgo(updated_time):
    now = datetime.now(timezone.utc)
    time_diff = now - updated_time
    seconds = int(time_diff.total_seconds())
    
    time_intervals = [
        (60, "second", seconds),
        (3600, "minute", seconds // 60),
        (86400, "hour", seconds // 3600),
        (2592000, "day", seconds // 86400),
        (31536000, "month", seconds // 2592000),
    ]

    for interval, label, value in time_intervals:
        if seconds < interval:
            return f"Updated {value} {label}{'s' if value != 1 else ''} ago"

    return f"Updated {seconds // 31536000} year{'s' if seconds // 31536000 != 1 else ''} ago"

def getMods():
    response = httpx.get("https://thunderstore.io/c/webfishing/api/v1/package/")
    response.raise_for_status()
    data = response.json()
    
    mods = {}
    for package in data:
        modPackage = str(package["full_name"])

        if modPackage not in mods:
            mods[modPackage] = {
                "uuid4": package["uuid4"],
                "modName": package["name"],
                "modAuthor": package["owner"],
                "modUrl": package["package_url"],
                "modTags": package["categories"],
                "modScore": package["rating_score"],
                "updatedAgo": timeAgo(datetime.fromisoformat(package['date_updated'].replace('Z', '+00:00'))),
                "isDeprecated": package['is_deprecated'],
                "isNSFW": package['has_nsfw_content'],
                "latestDownload": "",
                "latestDependencies": [],
                "totalDownloads": 0, 
                "versions": [],
            }

        latest_version = None
        for version in package['versions']:
            if latest_version is None or version['version_number'] > latest_version['version_number']:
                latest_version = version
            
            formedVersion = {
                "uuid4": version["uuid4"],
                "version": version["version_number"],
                "versionDownloads": version['downloads'],
                "modIcon": version["icon"],
                "modDownload": version["download_url"],
                "modDescription": version["description"],
                "active": version['is_active'],
                "fileSize": version['file_size'],
                "websiteUrl": version['website_url'],
                "dependencies": version["dependencies"]
            }
            mods[modPackage]["totalDownloads"] += version['downloads']
            mods[modPackage]["versions"].append(formedVersion)

        if latest_version:
            mods[modPackage]["latestWebsite"] = latest_version["website_url"]
            mods[modPackage]["latestDownload"] = latest_version["download_url"]
            mods[modPackage]["latestDependencies"] = latest_version["dependencies"]
            mods[modPackage]["latestVersion"] = latest_version["version_number"]

    return mods

# ONLY FOR DOWNLOADING MODS
def download(url, extractPath, data: dict = {}):
    print("Starting download...")

    with httpx.Client() as client:
        response = client.get(url, follow_redirects=True, timeout=60)
        response.raise_for_status()

        fileSize = int(response.headers.get('Content-Length', 0))
        downloadedSize = 0

        temp_folder = os.path.join(extractPath, "temp_extract")
        os.makedirs(temp_folder, exist_ok=True)

        with open(os.path.join(temp_folder, "mod.zip"), 'wb') as f:
            print("Downloading...")
            for chunk in response.iter_bytes(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloadedSize += len(chunk)
                    progress = (downloadedSize / fileSize) * 100 if fileSize else 0
                    print(f"Download progress: {progress:.2f}%")

    print("Download complete, extracting files...")
    
    with zipfile.ZipFile(os.path.join(temp_folder, "mod.zip")) as zip_ref:
        target_folder = None
        for file in zip_ref.namelist():
            if any(f in file for f in ["manifest.json", ".pck"]) and "/" in file:
                target_folder = os.path.dirname(file)
                break
        
        if not target_folder:
            print("No folder containing 'manifest.json' or '.pck' found; extracting root files.")
            target_folder = ""

        for file in zip_ref.namelist():
            if file.startswith(target_folder):
                destination_path = os.path.join(temp_folder, os.path.relpath(file, target_folder))
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                
                if not file.endswith('/'):
                    with open(destination_path, 'wb') as f:
                        f.write(zip_ref.read(file))

    modId = data.get("author", "") + "." + data.get("name", "")
    finalFolderPath = os.path.join(extractPath, modId if modId else "default")

    if os.path.exists(finalFolderPath):
        shutil.rmtree(finalFolderPath)

    os.rename(temp_folder, finalFolderPath)

    print(f"Mod extracted to '{finalFolderPath}' with {'modId: ' + modId if modId else 'no modId specified'}.")

    with open(os.path.join(finalFolderPath, "rnmInfo.json"), "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)

    print("Extraction complete.")

def downloadRaw(url: str, extractPath: str, data: dict = {}):
    with httpx.Client() as client:
        response = client.get(url, follow_redirects=True, timeout=60)
        response.raise_for_status()

        if response.status_code == 200:
            file_content = io.BytesIO(response.content)
            os.makedirs(extractPath, exist_ok=True)

            with zipfile.ZipFile(file_content) as zip_ref:
                zip_ref.extractall(extractPath)

            with open(os.path.join(extractPath, "rnmInfo.json"), "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                
            print(f"File successfully extracted to {extractPath}")
            
        else:
            print(f"Failed to download the file, status code {response.status_code}")