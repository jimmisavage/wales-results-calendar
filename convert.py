from ics import Calendar, Event
import requests

ics_url = "https://calendar.google.com/calendar/ical/f5vqdqdrbglm52e0na8jo9k4no%40group.calendar.google.com/public/basic.ics"
response = requests.get(ics_url)
calendar = Calendar(response.text)

new_calendar = Calendar()

for event in calendar.events:
    summary = event.name
    if summary and '(' in summary and ')' in summary:
        try:
            main_part, score_part = summary.rsplit('(', 1)
            score = score_part.strip(')').strip()
            if '-' not in score:
                continue

            teams = main_part.strip().split(' - ')
            if len(teams) == 2:
                home, away = teams
                new_summary = f"{home.strip()} {score} {away.strip()}"

                new_event = Event()
                new_event.name = new_summary
                new_event.begin = event.begin
                new_event.end = event.end
                new_event.uid = event.uid
                new_event.description = event.description
                new_event.location = event.location

                new_calendar.events.add(new_event)
        except:
            continue

with open("index.ics", "w") as f:
    f.write(str(new_calendar))
