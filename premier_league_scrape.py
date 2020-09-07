import requests
from bs4 import BeautifulSoup
import pandas as pd
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from email.mime.text import MIMEText
from pretty_html_table import build_table


def chosen_teams():

    Finlay = ['Arsenal', 'Leeds United' , 'Burnley', 'Fulham']
    Alasdair = ['Liverpool', 'Tottenham Hotspur', 'Newcastle United', 'Aston Villa']
    Reggie = ['Chelsea', 'Leicester City', 'Everton', 'Brighton and Hove Albion']
    Euan = ['Manchester United', 'Wolverhampton Wanderers', 'Southampton', 'West Ham United']
    Dad = ['Manchester City', 'Crystal Palace', 'Sheffield United', 'West Bromwich Albion']


    Fin_dict = {i: 'Finlay' for i in Finlay}
    Ali_dict = {i: 'Alasdair' for i in Alasdair}
    Reggie_dict =  {i: 'Reggie' for i in Reggie}
    Euan_dict =  {i: 'Euan' for i in Euan}
    Dad_dict =  {i: 'Dad' for i in Dad}

    players_dict = {**Fin_dict, **Ali_dict, **Reggie_dict, **Euan_dict, **Dad_dict}

    return players_dict

def scrape():
    url = "https://www.premierleague.com/tables"

    r1 = requests.get(url)
    r1.status_code

    coverpage = r1.content

    soup1 = BeautifulSoup(coverpage, 'html.parser')

    teams = []
    points = []

    for data in soup1.find_all('td', class_='team'):
        for a in data.find_all('span', class_='long'):
            teams.append(a.text)

    for data_1 in soup1.find_all('td', class_='points'):
            points.append(int(data_1.text))

    dictionary = dict(zip(teams, points))

    return dictionary

def create_comined_league_table():
    d1 = chosen_teams()
    d2 = scrape()

    ds = [d1, d2]
    d = {}
    for k in d1.keys():
        d[k] = tuple(d[k] for d in ds)

    combined_points_table = pd.DataFrame.from_dict(d, orient='index',
                           columns=['Player', 'Points'])
    combined_points_table.sort_values(by=['Points'])

    combined_points_table.index.name = 'Team'

    return combined_points_table

def create_player_standings():
    combined_league_table = create_comined_league_table()

    current_standings = combined_league_table.groupby(['Player'], as_index=False)['Points'].sum()
    return current_standings


def send_mail(body):

    message = MIMEMultipart()
    message['Subject'] = 'Boys_PL_Standings'
    message['From'] = 'euanjohnston92@gmail.com'
    message['To'] = 'euanjohnston92@gmail.com'

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], 'b1017535')
    server.sendmail(message['From'], message['To'], msg_body)
    server.quit()

def send_PL_update():
    df = create_player_standings()
    output = build_table(df, 'red_light',font_size = 'large', font_family = 'Times new Roman', text_align = 'left')
    send_mail(output)


send_PL_update()