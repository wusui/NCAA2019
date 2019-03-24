# NCAA March Madness office Pool Handler

Differences from previous versions:
  * Python 3
  * Uses requests library

## Before the tournament / Early in the tournament

cd to gen_data and perform the following tasks.

I still have not been able to put together a decent scraper for tournament
group parsing.  Using a browser, extract peoples picks and place them in
appropriately named directories in the members subdiretory (directory names
should match the corresponding group name with underscores replacing spaces).

Edit the groups.ini file to contain entries for each group that we are
monitoring.  Section names will contain the group name.  Each section will
contain one parameter named groupID that will contain the corresponding
groupID.

Run python check_all.py to make sure that the entries in members files are
valid.  These will be used later to extract pick information.

Generate a list of the sixty-four teams by running python get_teams.py after
all the playin games have been played. (Note: Needed to double check St vs.
State differences)

Make sure the sixty-four team list is sorted in bracket order (same order
that the teams would be listed in the bracket going top-to-bottom first).

At some point, run python extract_bracket.py.  This saves all the information
needed for later computations in group_picks.json.

From this point forward, we do not need to access the Espn site.

## During tournament (after first weekend)

cd figure_future

As the tournament progresses edit real_world.txt.  At the start of the
tournament, all 64 teams are listed in order.  After each round, there
is a blank  line and the winners of the next round are listed in order.

When the Sweet-16 round is reached, it becomes practical to generate
all possible results and see who wins.  Run gen_outcomes.py after the second,
third, and fourth rounds to generate result.json files.

cd display

Figure out good abbreviations for the schools and put them in the corresponding
locations in the abbrev.txt file.

Run bracket_display.py.  This creates html files that can be renamed
and displayed
