import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df,col):

    # Drop duplicates based on 'Year' and the specified column and Count the number of occurrences of each year
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values(by = 'Year')

    # Rename the columns appropriately
    nations_over_time.columns = ['Edition', col]

    return nations_over_time


def most_successful(df, sport):
    # Filter the DataFrame based on the selected sport
    temp_df = df[df['Sport'] == sport]

    # Count the number of occurrences of each Name
    name_counts = temp_df.dropna(subset=['Medal'])['Name'].value_counts().reset_index()

    # Rename the columns to avoid the 'index' KeyError
    name_counts.columns = ['Name', 'Count']

    # Get the top 15 most successful names
    top_names = name_counts.head(15)

    # Merge the top names with the original DataFrame to get additional information
    result = top_names.merge(df, left_on='Name', right_on='Name', how='left')

    # Select only the 'Name', 'Count', 'Sport', and 'Region' columns
    result = result[['Name', 'Count', 'Sport', 'region']].drop_duplicates()

    return result


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    # Count the number of occurrences of each Name
    name_counts = temp_df['Name'].value_counts().reset_index()

    # Rename the columns to avoid the 'index' KeyError
    name_counts.columns = ['Name', 'Medals']

    # Get the top 10 most successful names
    top_names = name_counts.head(10)

    # Merge the top names with the original DataFrame to get additional information
    result = top_names.merge(df, on='Name', how='left')

    # Select only the 'Name', 'Count', 'Sport', and 'Region' columns and remove duplicates
    result = result[['Name', 'Medals', 'Sport', 'region']].drop_duplicates()

    return result.head(10)


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
