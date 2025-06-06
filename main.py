import requests
import time

# Plugins to monitor: {project_id: last_known_version_id}
PLUGINS = {
    "OwqSnlXx": None,  # AevorinReports
    "CWMrVT99": None  # FlyCraft
}

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."  # Replace with your actual webhook
CHECK_INTERVAL = 300  # 5 minutes

def get_latest_version(project_id):
    url = f"https://api.modrinth.com/v2/project/{project_id}/version"
    response = requests.get(url)
    if response.status_code == 200:
        versions = response.json()
        if versions:
            return versions[0]
    return None

def send_discord_message(project_id, version):
    embed = {
        "title": f"🔔 New Update: {version['name']}",
        "description": (
            f"**Project:** `{project_id}`\n"
            f"[Download here]({version['files'][0]['url']})\n\n"
            f"**Version:** {version['version_number']}\n"
            f"**Date:** {version['date_published']}"
        ),
        "color": 0x00ff00
    }
    data = {
        "username": "Modrinth Updates",
        "embeds": [embed]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

while True:
    for project_id in PLUGINS:
        version = get_latest_version(project_id)
        if version:
            current_id = PLUGINS[project_id]
            if version["id"] != current_id:
                PLUGINS[project_id] = version["id"]
                send_discord_message(project_id, version)
    time.sleep(CHECK_INTERVAL)