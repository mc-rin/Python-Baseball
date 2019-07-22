import pandas as pd
import matplotlib.pyplot as plt

from data import games

plays = games[games['type'] == 'play']
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches',
                 'event', 'game_id', 'year']

# These functions select the rows where the event column's value starts with S
# (not SB), D, T, and HR in the plays DataFrame to create the hits DataFrame.
hits = plays.loc[plays['event'].str.contains('^(?:S(?!B)|D|T|HR)'),
                 ['inning', 'event']]
# This function converts the inning column of the hits DataFrame from
# strings to numeric.
hits.loc[:, 'inning'] = pd.to_numeric(hits.loc[:, 'inning'])

# The event column of the hits DataFrame now contains event information of
# various configurations. It contains where the ball was hit and other
# information that is not needed. This will be replaced with the type of hit
# for grouping later on.
replacements = {r'^S(.*)': 'single',
                r'^D(.*)': 'double',
                r'^T(.*)': 'triple',
                r'^HR(.*)': 'hr'}

hit_type = hits['event'].replace(replacements, regex=True)

hits = hits.assign(hit_type=hit_type)
# The DataFrame becomes a groupby object that also contains a new column
# that counts the number of hits per inning, which is then converted to a
# DataFrame.
hits = hits.groupby(['inning', 'hit_type']).size().reset_index(name='count')
# pd.Categorical saves memory by making hits['hit_type'] a categorical column.
hits['hit_type'] = pd.Categorical(hits['hit_type'], ['single', 'double',
                                                     'triple', 'hr'])
# This operation sorts the values in the DataFrame by inning and hit type.
hits = hits.sort_values(['inning', 'hit_type'])
# The pivot function is used to reshape the hits DataFrame for plotting.
hits = hits.pivot(index='inning', columns='hit_type', values='count')

# The data will be displayed as a stacked bar chart.
hits.plot.bar(stacked=True)
plt.show()
