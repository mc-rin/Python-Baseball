import pandas as pd
import matplotlib.pyplot as plt

from data import games

plays = games[games['type'] == 'play']

strike_outs = plays[plays['event'].str.contains('K')]
# The DataFrame becomes a groupby object that also contains a new column that
# displays the number of strikeouts in the game.
strike_outs = strike_outs.groupby(['year', 'game_id']).size()
# The groupby object is converted to a DataFrame
strike_outs = strike_outs.reset_index(name='strike_outs')
# loc[] selects all rows and the year and strike_outs columns of the DataFrame
# and the two selected columns' values are are converted to numeric.
strike_outs = strike_outs.loc[:, ['year',
                                  'strike_outs']].apply(pd.to_numeric)

strike_outs.plot(x='year', y='strike_outs',
                 kind='scatter').legend(['Strike Outs'])
plt.show()
