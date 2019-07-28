import pandas as pd
import matplotlib.pyplot as plt

from frames import games, info, events

plays = games.query("type == 'play' & event != 'NP'")
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches',
                 'event', 'game_id', 'year']

# The shift() function moves the index a specified amount up or down. The
# following row condition selects all rows that do not match a consecutive
# row in the player column.
pa = plays.loc[plays['player'].shift() != plays['player'],
               ['year', 'game_id', 'inning', 'team', 'player']]
# The DataFrame becomes a groupby object that also contains a new column
# that calculates the plate appearance for each team for each game, which is
# then converted to a DataFrame.
pa = pa.groupby(['year', 'game_id', 'team']).size().reset_index(name='PA')

# Set the index of the events DataFrame to four columns.
events = events.set_index(['year', 'game_id', 'team', 'event_type'])
# The events DataFrame is unstacked.
events = events.unstack().fillna(0).reset_index()
# The column labels are managed.
events.columns = events.columns.droplevel()
events.columns = ['year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR',
                  'ROE', 'SO']
events = events.rename_axis(None, axis='columns')

# The DataFrames containing the plate appearances data are merged.
events_plus_pa = pd.merge(events, pa, how='outer',
                          left_on=['year', 'game_id', 'team'],
                          right_on=['year', 'game_id', 'team'])

# The DataFrames containing team data are merged to determine which league
# was the home team and which was the visiting team.
defense = pd.merge(events_plus_pa, info)
# The Defense Efficiency Ratio (DER), which is a metric to gauge team
# defense, is calculated.
defense.loc[:, 'DER'] = 1 - ((defense['H'] + defense['ROE']) / (defense[
    'PA'] - defense['BB'] - defense['SO'] - defense['HBP'] - defense['HR']))
defense.loc[:, 'year'] = pd.to_numeric(defense['year'])

# The DER DataFrame is reshaped to allow the DER of the All-star teams in
# the last 40 years to be plotted.
der = defense.loc[defense['year'] >= 1978, ['year', 'defense', 'DER']]
der = der.pivot(index='year', columns='defense', values='DER')

# The DER plot is plotted with the default line plot type.
der.plot(x_compat=True, xticks=range(1978, 2018, 4), rot=45)
plt.show()
