import argparse
import requests as req
import browser_cookie3
import warnings


class Stage:
    def __init__(self, seg_id, cj):
        self.seg_id = seg_id
        # self.name = get_segment_name(seg_id, cj)


class Activity:
    def __init__(self, act_id, cj):
        self.stage_times = []
        self.act_id = act_id
        # self.name = get_athlete_name(act_id, cj)


class Race:
    def __init__(self, name, cj):
        self.activities = []
        self.stages = []
        self.name = name
        self.cj = cj

    def add_stage(self, seg_id):
        if validate_id(seg_id, 'segments', self.cj):
            self.stages.append(Stage(seg_id, self.cj))
        else:
            warnings.warn(f'Segment with id "{seg_id}" was not found. Skipping stage...')

    def add_activity(self, act_id):
        if validate_id(act_id, 'activities', self.cj):
            self.activities.append(Activity(act_id, self.cj))
        else:
            warnings.warn(f'Activity with id "{act_id}" was not found. Skipping activity...')

    def get_segment_times(self):
        for activity in self.activities:
            for stage in self.stages:
                # activity.stage_times.append(get_stage_time(stage.seg_id, self.cj))



# Validate that segment or activity ID exists
# type should be either 'activities' or 'segments'
def validate_id(id, type, cj):
    res = req.get(f'https://www.strava.com/{type}/{id}/', cookies=cj)
    if res.status_code == 200:
        return True
    return False


# Exports Strava.com cookies from the chosen browser
def get_strava_cookies(browser):
    domain = 'www.strava.com'
    if browser == 'firefox':
        return browser_cookie3.firefox(domain_name=domain)
    if browser == 'chrome':
        return browser_cookie3.chrome(domain_name=domain)
    if browser == 'opera':
        return browser_cookie3.opera(domain_name=domain)
    if browser == 'edge':
        return browser_cookie3.edge(domain_name=domain)


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
    cj = get_strava_cookies(args.browser)
    r = Race(args.name, cj)

    print(validate_id('6658948635', 'activities', cj))
