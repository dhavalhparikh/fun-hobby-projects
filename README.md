# fun-hobby-projects
A repo for my hobby projects done in spare time

## USCIS case status checker
A simple script to retrieve the USCIS case status without going to the website.
It's very boring to go to the USCIS website and enter the 13-digit case number
and then get the status. So I automated it! I make POST request to the uscis page with the case number,
use beautiful soup to extract the required data and details, (optional) use the
IFTTT maker channel to send the details about my case status to my phone via SMS

This script can also be added in a cron job and have a raspberry pi run it periodically
for eg. once every hour from 10 AM - 8 PM everyday to make our lives easier

(optional) A receipe can also be created on IFTTT to send to send these details
to a Slack channel. For eg. If Maker then Slack

Do read the comments in the script!

### Python package requirements
BeautifulSoup - `sudo pip install beautifulsoup`
Requests - `sudo pip install requests`

## mqtt client
An MQTT based client to listen to specific topics published by a MQTT broker.

## Beebotte REST API tester
A simple python script to test the [Beebotte](https://beebotte.com/) REST API.
Replace the `API_KEY` and `SECRET_KEY` with your own keys.
Also change the `channel` and `resource` as defined in your dashboard.
