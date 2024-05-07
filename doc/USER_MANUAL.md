# User manual

WebAppRadar provides HTTP API for user interaction.

**You can access the Swagger UI documentation** with examples on `<url>:<port>` of WebAppRadar (see [installation manual](INSTALL_MANUAL.md) for configuring the port) using your web browser.

## Running the scan
WebAppRadar tries to discover all web applications running in network range given by a user as input.
The scan compares the found information with latest web app releases.

To run the scan you should use POST method with `/scan` endpoint and provide the subnets or IP addresses (or combination of both)
that will be scanned in form of request body:
```json
{
  "subnets": "192.168.0.0/24,192.168.68.68"
}
```
Example: Sending POST request to `<web_app_url>/scan` with the body above will trigger scan of whole `192.168.0.0/24` subnet 
and `192.168.68.68` IP address. Only the web applications deployed and running on these addresses will be included in the result.

The response will include a unique ID assigned to the scan which can be later used for getting the scan result.

IMPORTANT NOTE: **Only one scan be running at a time.** If another scan in the process, a response with 409 status code is returned. 

## Getting the results

You can list all finished scans using GET request on `/result` URL.

These results will NOT include the main information about the web application, but rather just the complete list of scan IDs, times of scan 
competition and the scan statuses. Example:
```json
[
  {
    "id": "471edecd-6f4a-4bf1-bc50-7aeb1a6af79a",
    "completed_at": "2024-04-13T19:40:36.323496",
    "status": "success"
  },
  {
    "id": "5432daad-6aaa-4bc4-1234-abc8646af666",
    "completed_at": "2024-03-25T19:35:02.123456",
    "status": "fail"
  }
]
```

To see the cause of `status: fail` you have to read the app [logs](INSTALL_MANUAL.md).

To list the complete result of a specific scan, user can use GET request on `/result/<id>` URL where id is the ID of the scan.
Example of the response:
```json
{
  "id": "35c92f44-c4a7-47f1-9a19-fc2f9d81b5ba",
  "completed_at": "2024-04-15T12:13:42.434006",
  "status": "success",
  "subnets": "192.168.0.0/24,192.168.68.68",
  "web_apps": [
    {
      "hostname": "jira.example.org",
      "name": "Jira",
      "version": "5.1.1",
      "latest_version": "7.2.3",
      "latest_cycle_version": "5.1.9",
      "eol": false,
      "eol_date": "2024-04-15"
    },
    {
      "hostname": "docu.example.org",
      "name": "Confluence",
      "version": "8.2.5",
      "latest_version": "8.2.5",
      "latest_cycle_version": "8.2.5",
      "eol": null,
      "eol_date": null
    },
    {
      "hostname": "rail-page.io",
      "name": "TestRail",
      "version": "6.0.0",
      "latest_version": "7.0.0",
      "latest_cycle_version": null,
      "eol": null,
      "eol_date": null
    },
    {
      "hostname": "git.example.org",
      "name": "GitLab",
      "version": "14.5.19",
      "latest_version": null,
      "latest_cycle_version": null,
      "eol": null,
      "eol_date": null
    },
    {
      "hostname": "nms.example.com",
      "name": "Zabbix",
      "version": null,
      "latest_version": null,
      "latest_cycle_version": null,
      "eol": null,
      "eol_date": null
    },
    {
      "hostname": "super-web-page.example.org",
      "name": null,
      "version": null,
      "latest_version": null,
      "latest_cycle_version": null,
      "eol": null,
      "eol_date": null
    }
  ]
}
```
- `hostname`: Hostname of the scanned device
- `name`: Name of the web application (nullable)
- `version`: Current version of the web application (nullable)
- `latest_version`: Latest available version of the web application (nullable)
- `latest_cycle version`: Latest version of the web application regarding the current cycle version (MAJOR.MINOR) (nullable)
- `eol`: Flag indicating whether the current version reached EOL support (nullable)
- `eol_date`: End of Life date of the current version (nullable)

For more information please open the Swagger UI documentation running on `<url>:<port>` of the WebAppRadar app.