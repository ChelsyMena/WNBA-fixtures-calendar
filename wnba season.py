# -*- coding: utf-8 -*-
"""
Author: Chelsy Mena
GitHub: @ChelsyMena 

"""
import pandas as pd
#%%

#We have a .txt with the fixtures of the WNBA's 25th season. 
# We want .csv files that can be converted to .ics for calendars to read

# We extract each line from the txt to an empty list
mylines = []
with open ('wnba season.txt', 'rt') as myfile:  # Open file lorem.txt
    for line in myfile:
        mylines.append(line)
#%%
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']

#%% #We have dates for each day, we get how many games there are in each date
dates = []
n_games = []
for i in range(len(mylines)):
    for day in days:
        if day in mylines[i]:
            dates.append(mylines[i])
            n_games.append(mylines[i+1])
#%% #We don't need the word game in there, just the number
n_games = pd.DataFrame(n_games)
n_games[0] = n_games[0].astype(str)
n_games[0] = n_games[0].str.replace(' Games\n',' ')
n_games[0] = n_games[0].str.replace(' Game\n',' ')
#%% Get the game times
game_times = []
for i in range(len(mylines)):
    if ' ET' in mylines[i]:
        game_times.append(mylines[i])
 
game_times = pd.DataFrame(game_times)
game_times[0] = game_times[0].str.replace(' ET','')
game_times[0] = game_times[0].str.replace('\n','')
game_times[0] = game_times[0].str.replace(' pm',' PM')

#%% We create the end times for all these games as well

#Get just the o'clock hour and add 2
starts = game_times.copy()
starts[0] = starts[0].str.replace(':00 PM', '')
starts[0] = starts[0].str.replace(':30 PM', '')
end_times = []
for i in range(len(starts)):
    entry = int(starts[0][i]) + 2
    end_times.append(entry)

# GLue them with the entire start time in case it was a half hour time
end_times = pd.DataFrame(end_times)
for i in range(len(end_times)):
    end_times[0][i] = f'{end_times[0][i]}{game_times[0][i]}'

#delete the bit of the start's o'clock hour from the end time
for i in range(len(end_times)):
    end_times[0][i] = end_times[0][i].replace(f'{starts[0][i]}', '')
#%% Now we need to get the teams in each fixture
teams = ['Atlanta Dream',
         'Chicago Sky',
         'Connecticut Sun',
         'Dallas Wings',
         'Indiana Fever',
         'Las Vegas Aces',
         'Los Angeles Sparks',
         'Minnesota Lynx',
         'New York Liberty',
         'Washington Mystics',
         'Phoenix Mercury',
         'Seattle Storm']
#%%
mylines = pd.DataFrame(mylines)
mylines[0] = mylines[0].str.replace('\n','')
#%%
fixtures = []
for i in range(len(mylines)):
    for team in teams:
        if ((team in mylines[0][i]) and (mylines[0][i+1] in teams)):
            fixture = f'{mylines[0][i]} @ {mylines[0][i+1]}'
            fixtures.append(fixture)
#%% getting the dates for all games using the date and the number of games per night

dates_fleshed_out = []
i = 0
for date in dates:
    n = int(n_games[0][i])
    dates_fleshed_out += n*[date]
    i += 1
# Fixing the date format
dates_fleshed_out = pd.DataFrame(dates_fleshed_out)
for day in days:
    dates_fleshed_out[0] = dates_fleshed_out[0].str.replace(f'{day}, ','')

months = ['May','June','July','August','September']
months_number =['05/','06/','07/','08/','09/',]

k = 0
for month in months:
   for i in range(len(dates_fleshed_out)):
       if month in dates_fleshed_out[0][i]:
           dates_fleshed_out[0] = dates_fleshed_out[0].str.replace(f'{month} ',f'{months_number[k]}')
           k += 1

dates_fleshed_out[0] = dates_fleshed_out[0].map(lambda x: x+'/2021')
dates_fleshed_out[0] = dates_fleshed_out[0].str.replace('\n','')

#%% There are still some missing columns for a good .csv turned .ics, we define them
category = ['WNBA']*192
dates_fleshed_out = list(dates_fleshed_out[0])
game_times = list(game_times[0])
end_times = list(end_times[0])
all_day = ['No']*192
duration = ['2 hours']*192
timezone = ['Eastern Time']*192

#%% Google Calendar only uses some anyway, we make the df with those

season_games = pd.DataFrame(data = {'Subject':fixtures, 
                                    #'Category':category,
                                    'Start Date':dates_fleshed_out,
                                    'Start Time':game_times, 
                                    'End Date':dates_fleshed_out,
                                    'End Time':end_times})
                                    #'Duration':duration})
                                    #'Timezone':timezone})
#%% #Finaly, we can create a .csv with the fixtures for each team
for team in teams:
    newdf = season_games[season_games.Subject.str.contains(team)]
    newdf.to_csv(f'{team}_season.csv', index = False)
    
#%% And a final .csv with all the fixtures if you don't particularly rep any team (like me)
season_games.to_csv(r'wnba_season.csv', index = False)