import io
import os
import json
import httpx
import zipfile
from datetime import datetime, timezone

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

# what im trying to do here is get where the mod stuff is stored
# usually looking for the mod folder and its content inside the folder ONLY
# unzip the mod folder to the extract path and done
# but it unfortunately does not wanna work properly sometimes due to
# modders just dumping the fuck out of their mods in THE MODS FOLDER WITHOUT MAKING A SUBFOLDER FOR IT
# OR EVEN MAKE IT PROPER IN GENERAAAALLLL

# notnite please enforce a proper mod file structure

def download(url, extractPath, data: dict = {}):
    response = httpx.get(url, follow_redirects=True)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        extractFolder = None
        for file in zip_ref.namelist():
            if 'manifest.json' in file and file.count('/') > 1:
                extractFolder = file.split('manifest.json')[0]
                break
        
        if extractFolder is None:
            print("No folder containing 'manifest.json' found")
            extractFolder = ""

        try:
            folderName = os.path.basename(extractFolder.rstrip('/'))
            extractedFolder = os.path.join(extractPath, folderName)
        except AttributeError:
            print("folder to extract is none.")
            return 
        
        for file in zip_ref.namelist():
            if file.startswith(extractFolder):
                file_relative_path = os.path.relpath(file, extractFolder)
                destination_path = os.path.join(extractPath, folderName, file_relative_path)
                
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                if not file.endswith('/'):
                    with open(destination_path, 'wb') as f:
                        f.write(zip_ref.read(file))

        manifest_local_path = os.path.join(extractedFolder, 'manifest.json')
        with open(manifest_local_path, 'r', encoding='utf-8') as manifest_file:
            manifest_data = json.load(manifest_file)
            modId = manifest_data.get('Id')

        if modId:
            folderPath = os.path.join(extractPath, modId)
            os.rename(extractedFolder, folderPath)
            print(f"Folder '{folderName}' renamed to '{modId}' and extracted successfully to {extractPath}")

            with open(f"{folderPath}\\rnmInfo.json", "w") as f:
                json.dump(data, f, indent=4)
        else:
            print(f"No 'Id' found in manifest.json; folder extracted as '{folderName}'.")

            with open(f"{extractPath}\\rnmInfo.json", "w") as f:
                json.dump(data, f, indent=4)