import pandas as pd
import matplotlib.pyplot as plt

from data import games

# loc[] returns the new selection as a DataFrame.
attendance = games.loc[(games['type'] == 'info') &
                       (games['multi2'] == 'attendance'), ['year', 'multi3']]
attendance.columns = ['year', 'attendance']

# loc[] selects all rows and just the attendance column
# of the attendance DataFrame, which is then converted to a numeric type.
attendance.loc[:, 'attendance'] = pd.to_numeric(attendance.loc[
                                                :, 'attendance'])
# plt() creates a plot of the attendance DataFrame
attendance.plot(x='year', y='attendance', figsize=(15, 7), kind='bar')

# The following two functions label the x and y axis.
plt.xlabel('Year')
plt.ylabel('Attendance')
# The following function draws a dashed green line
# perpendicular to the x-axis at the mean.
plt.axhline(y=attendance['attendance'].mean(), label='Mean',
            linestyle='--', color='green')
plt.show()
