import httpx
import json
from datetime import datetime, timezone


def time_ago(updated_time):
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

def parse_packages(packages):
    modList = {}
    for package in packages:
        modPackage = str(package["full_name"])

        if modPackage not in modList:
            modList[modPackage] = {
                "uuid4": package["uuid4"],
                "modName": package["name"],
                "modAuthor": package["owner"],
                "modUrl": package["package_url"],
                "modTags": package["categories"],
                "modScore": package["rating_score"],
                "updatedAgo": time_ago(datetime.fromisoformat(package['date_updated'].replace('Z', '+00:00'))),
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
            modList[modPackage]["totalDownloads"] += version['downloads']
            modList[modPackage]["versions"].append(formedVersion)

        if latest_version:
            modList[modPackage]["latestDownload"] = latest_version["download_url"]
            modList[modPackage]["latestDependencies"] = latest_version["dependencies"]

    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(modList, json_file, indent=4)


if __name__ == "__main__":
    try:
        response = httpx.get("https://thunderstore.io/c/webfishing/api/v1/package/")
        response.raise_for_status()
        data = response.json()
        parse_packages(data)
    except httpx.RequestException as e:
        print(f"Error fetching data: {e}")