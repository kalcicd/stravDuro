import argparse
import json
import requests as req
import re
import browser_cookie3
import xlsxwriter


class Stage:
    def __init__(self, seg_id, cj):
        self.seg_id = seg_id
        self.seg_link = f'https://www.strava.com/segments/{seg_id}/'

        html_text = req.get(self.seg_link, cookies=cj).text

        # This regex selects the segment name
        seg_re = '(?<=segmentName: ")(.*?)(?=")'
        self.name = re.search(seg_re, html_text).group(0)


class Activity:
    def __init__(self, act_id, cj):
        self.stage_times = []
        self.act_id = act_id
        self.act_link = f'https://www.strava.com/activities/{act_id}/'

        html_text = req.get(self.act_link, cookies=cj).text

        # This regex selects the unparsed json for all the activity's segments
        seg_re = '(?<=pageView\.segmentEfforts\(\)\.reset\()(.*)(?=, { parse: true }\);)'
        self.segments_json = json.loads(re.search(seg_re, html_text).group(0))

        # This regex selects the unparsed json for the activity athlete.
        ath_re = '(?<=activityAthlete = new Strava\.Models\.Athlete\()(.*)(?=\);)'
        self.name = json.loads(re.search(ath_re, html_text).group(0))['display_name']


class Race:
    def __init__(self, name, cj):
        self.activities = []
        self.stages = []
        self.name = name
        self.cj = cj

    def add_stage(self, seg_id):
        if validate_id(seg_id, 'segments', self.cj):
            self.stages.append(Stage(seg_id, self.cj))
            print(f'Segment with id "{seg_id}" added to the course...')
        else:
            print(f'WARNING: Segment with id "{seg_id}" was not found. '
                  f'Skipping stage...')

    def add_activity(self, act_id):
        if validate_id(act_id, 'activities', self.cj):
            self.activities.append(Activity(act_id, self.cj))
            print(f'Activity with id "{act_id}" added to the race...')
        else:
            print(f'WARNING: Activity with id "{act_id}" was not found. '
                  f'Skipping activity...')

    # Parses through activities' matched segments for the race stages, then
    # saves the stage times in the Race object state
    def get_segment_times(self):
        for activity in self.activities:
            dnf = False
            total_time = 0
            for stage in self.stages:
                all_efforts = activity.segments_json['efforts'] + \
                              activity.segments_json['hidden_efforts']
                seg_found = False
                for segment in all_efforts:
                    if segment['segment_id'] == stage.seg_id:
                        seg_found = True
                        activity.stage_times.append({
                            'id': stage.seg_id,
                            'name': stage.name,
                            'time': segment['elapsed_time'],
                            'time_raw': segment['elapsed_time_raw']
                        })
                        total_time += segment['elapsed_time_raw']
                if not seg_found:
                    print(f'WARNING: Activity {activity.act_id} does not '
                          f'contain segment {stage.seg_id}. Marking as DNF...')
                    activity.stage_times.append({
                        'id': stage.seg_id,
                        'name': stage.name,
                        'time': 'DNF',
                        'time_raw': 'DNF',
                    })
                    dnf = True
            if dnf:
                activity.total_time = 'DNF'
            else:
                activity.total_time = total_time

    # Exports the state of the Race object to a xlsx spreadsheet
    def export(self):
        title = f'{self.name}_results.xlsx'.replace(' ', '_')
        workbook = xlsxwriter.Workbook(title)
        worksheet = workbook.add_worksheet()

        worksheet.write(1, 0, 'Stages')
        worksheet.write(0, 1, 'Athletes')

        # Add stage labels
        col = 2
        for stage in self.stages:
            worksheet.write(1, col, stage.name)
            col += 1
        worksheet.write(1, col, 'TOTAL')

        workbook.close()
        print('Race Results successfully exported!')


# Validate that segment or activity ID exists
# type should be either 'activities' or 'segments'
def validate_id(id, type, cj):
    res = req.get(f'https://www.strava.com/{type}/{id}/', cookies=cj)
    if res.status_code == 200:
        return True
    return False


# Gets Strava.com cookies from the chosen browser
def get_strava_cookies(browser):
    domain = '.strava.com'
    if browser == 'firefox':
        return browser_cookie3.firefox(domain_name=domain)
    if browser == 'chrome':
        return browser_cookie3.chrome(domain_name=domain)
    if browser == 'opera':
        return browser_cookie3.opera(domain_name=domain)
    if browser == 'edge':
        return browser_cookie3.edge(domain_name=domain)


# Gathers info from command line args
def parse_cl_args():
    d = 'StravDuro: a tool to hold your own Strava Enduro!'
    u = 'stravDuro.py [--name] N [--activities] A [--segments] S [--browser]' \
        ' B\n Note: The order in which the segment IDs are entered ' \
        'determines the stage number.'
    parser = argparse.ArgumentParser(description=d, usage=u)
    parser.add_argument('--name', metavar='N', nargs=1, required=True,
                        type=str)
    parser.add_argument('--activities', metavar='A', nargs='+', required=True,
                        type=int)
    parser.add_argument('--segments', metavar='S', nargs='+', required=True,
                        type=int)
    parser.add_argument('--browser', metavar='B', nargs=1, required=True,
                        choices=['chrome', 'firefox', 'opera', 'edge'])
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_cl_args()

    # Use cookies from our browser that is logged in to Strava so we can view
    # segments and activities
    cj = get_strava_cookies(args.browser[0])
    r = Race(args.name[0], cj)
    for seg_id in args.segments:
        r.add_stage(seg_id)
    for act_id in args.activities:
        r.add_activity(act_id)
    r.get_segment_times()
    r.export()
