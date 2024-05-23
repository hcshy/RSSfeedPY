# RSS Feed Server

This project is a simple HTTPS server that serves an RSS feed and allows clients to post new items to the feed.

## Features

- **HTTPS Support**: The server supports HTTPS, ensuring secure communication with clients.
- **RSS Feed Generation**: Generates an RSS feed with sample items.
- **POST Endpoint**: Provides an endpoint for clients to post new items to the RSS feed.
- **Configuration File**: Uses a `settings.conf` file to configure server settings such as host, port, and certificate paths.

## Requirements

- Python 3.x
- PyInstaller (if building as an executable)

## Installation

1. Clone the repository or download the release.

2. Configuration

Create a new settings.conf file or modify the existing one according to your preferences. The settings.conf file should include the following parameters:
```
[Server]
host:localhost                   #The hostname or IP address where you want the server to run (e.g., localhost).
port:8080                        #The port number where you want the server to listen for incoming connections (e.g., 8080).
certfile:<path_to_cert>          #The path to the SSL certificate file (e.g., localhost.crt).
keyfile:<path_to_key>            #The path to the SSL key file (e.g., localhost.key).
```

Place the settings.conf file in the same directory as the python script. 

Run the python script. The server will start listening for incoming connections based on the settings specified in the settings.conf file.

That's it! You should now have the server running with the configurations specified in the settings.conf file. You can access the server using the specified hostname, port, and SSL certificate.

### Posting a Request to `/rssitem/`

Clients can post new items to the RSS feed by sending a POST request to the `/rssitem/` endpoint. Here's how you can do it using Python's `requests` library:

```python
import requests
import json

# Define the URL of the server
url = "https://<server-host>:<server-port>/rssitem/"

# Define the JSON data for the new RSS item
new_item = {
    "Title": "New RSS Item",
    "Description": "Description of the new item",
    "Link": "https://example.com/new-item"
}

# Convert the JSON data to a string
data = json.dumps(new_item)

# Set the headers to specify the content type
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, data=data, headers=headers)

# Check the response status
if response.status_code == 200:
    print("RSS item added successfully.")
else:
    print("Failed to add RSS item:", response.text)
```

Contributing
Contributions are welcome! Please open an issue or submit a pull request with any improvements or fixes.

