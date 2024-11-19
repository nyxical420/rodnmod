from json import dump
from io import BytesIO
from shutil import rmtree
from zipfile import ZipFile
from httpx import get, Timeout
from datetime import datetime, timezone
from os import path, makedirs, rename, remove

timeout = Timeout(60, read=None)

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
    response = get("https://thunderstore.io/c/webfishing/api/v1/package/", timeout=timeout)
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

    response = get(url, follow_redirects=True, timeout=timeout)
    response.raise_for_status()

    temp_folder = path.join(extractPath, "temp_extract")
    makedirs(temp_folder, exist_ok=True)

    with open(path.join(temp_folder, "mod.zip"), 'wb') as f:
        print("Downloading...")
        for chunk in response.iter_bytes(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print("Download complete, extracting files...")
    
    with ZipFile(path.join(temp_folder, "mod.zip")) as zip_ref:
        target_folder = None
        for file in zip_ref.namelist():
            if any(f in file for f in ["manifest.json", ".pck"]) and "/" in file:
                target_folder = path.dirname(file)
                break
        
        if not target_folder:
            print("No folder containing 'manifest.json' or '.pck' found; extracting root files.")
            target_folder = ""

        for file in zip_ref.namelist():
            if file.startswith(target_folder):
                destination_path = path.join(temp_folder, path.relpath(file, target_folder))
                makedirs(path.dirname(destination_path), exist_ok=True)
                
                if not file.endswith('/'):
                    with open(destination_path, 'wb') as f:
                        f.write(zip_ref.read(file))

    modId = data.get("author", "") + "." + data.get("name", "")
    finalFolderPath = path.join(extractPath, modId if modId else "default")

    if path.exists(finalFolderPath):
        rmtree(finalFolderPath)

    rename(temp_folder, finalFolderPath)

    print(f"Mod extracted to '{finalFolderPath}' with {'modId: ' + modId if modId else 'no modId specified'}.")

    with open(path.join(finalFolderPath, "rnmInfo.json"), "w", encoding='utf-8') as f:
        dump(data, f, indent=4)

    if path.exists(finalFolderPath + "\\\\mod.zip"):
        remove(finalFolderPath + "\\\\mod.zip")

    if path.exists(temp_folder):
        rmtree(temp_folder)

    print("Extraction complete.")

def downloadRaw(url: str, extractPath: str, data: dict = {}):
    response = get(url, follow_redirects=True, timeout=timeout)
    response.raise_for_status()

    if response.status_code == 200:
        makedirs(extractPath, exist_ok=True)

        try:
            with ZipFile(BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(extractPath)

            if data:
                json_path = path.join(extractPath, "rnmInfo.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    dump(data, f, indent=4)

            print(f"File successfully downloaded and extracted to {extractPath}")
        except Exception as e:
            print(f"Error during extraction: {e}")
    else:
        print(f"Failed to download the file, status code {response.status_code}")