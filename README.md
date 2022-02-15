# StravDuro v1
#### Hold an enduro race with your friends using Strava!

## What is StravDuro?
StravDuro is a simple Python script that looks through a list of Strava activities, gathers segment times for a select set of segments, then outputs the results to an easy-to-view spreadsheet.

## Disclaimer
This project is completely unaffiliated with Strava. Bike racing is an inherently dangerous and risky activity. By using this tool, you agree to ride responsibly and not hold the StravDuro developers or Strava liable for any damages or injuries that may occur during your ride. Mmmkay?

## How to Use this Script:
### Prerequisites
* Python 3 or later
* pip3 (should come with your Python 3 Installation)
* A web browser that is logged in to Strava (more on this in the --browser section)

Install the required modules:
    
    pip3 install -r ./requirements.txt

### Running the Script
    python3 ./stravDuro.py --name "race title" --activities . . . --segments . . . --browser [firefox | chrome | opera | edge]
StravDuro must be run with the required `--name`, `--activities`, `--segments`, and `--browser` flags:
#### --name
Following the `--name` flag should be a **quotation-wrapped** title for the race.

#### --activities
Following the `--activities` flag should be a **space-separated** list of Strava activity IDs to be entered into the race. An activity's ID can be found after the `/activities/` part in its URL.

    https://www.strava.com/activities/5678626826
In the above ride URL example, `5678626826` is the activity ID

#### --segments
Similarly to the activities flag, the `--segments` flag should be followed by a **space-separated** list of Strava segment IDs to be added to the race course. A segment's ID can be found after the `/segments/` part in its URL.

***IMPORTANT NOTE ABOUT SEGMENT IDs:*** If you click on a segment from an activity page, you might notice `/segments/2853984407537277732` or similar is appended to the activity URL. This does *NOT* contain the segment's true ID. This is the effort ID, which refers to the specific instance the segment was ridden, not the segment itself. To get to the URL with the correct segment ID, click on the "View full leaderboard" button.

    https://www.strava.com/segments/29191644?filter=overall
In the above segment URL example, `29191644` is the segment ID

#### --browser
If you are an anonymous Strava browser, you are unable to view any segment or activity data. Instead, you are given a prompt to log in or sign up. To get around this, we need to use the browser's Strava cookie so the script can access data that a logged-in user could see. **Make sure you are logged in to Strava on your browser of choice before running this script!** Supported options for the `--browser` flag are the following:
* `firefox`
* `chrome`
* `opera`
* `edge`

### Output
Once the script is finished running, a `your_race_title_here.xlsx` spreadsheet file will be created in the working directory of the script.
