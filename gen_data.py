#!/usr/bin/env python3

import pandas as pd
import numpy as np
import random
from tqdm import tqdm
from geopy.distance import geodesic

def random_dates(start, end, n=10):
    start_u = start.value//10**9
    end_u = end.value//10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

def count_cost(start_time, distance):
    cost = 2 + 0.5 * distance
    if (start_time.hour >= 8 and start_time.hour <= 9) or \
        (start_time.hour >= 18 and start_time.hour <= 19):
        cost *= 1.5
    if (start_time.hour >= 22 or start_time.hour <= 6):
        cost *= 1.3
    return cost


df = pd.read_csv("London postcodes.csv", delimiter=',')
rides = pd.DataFrame(columns=['driver_id', 'client_id',\
                              'start', 'start_latitude', 'start_longtitude', \
                              'finish', 'finish_latitude', 'finish_longtitude', \
                              'distance', 'road_time', 'start_time', 'finish_time', 'cost', \
                              'driver_rate', 'category_driver_feedback', 'text_driver_feedback',\
                             'client_rate', 'category_client_feedback', 'text_client_feedback'])
NUM_RIDES = 5000000
rides['driver_id'] = np.random.randint(low=0, high=2500, size=NUM_RIDES)
rides['client_id'] = np.random.randint(low=0, high=4500, size=NUM_RIDES)
rides[['start', 'start_latitude', 'start_longtitude']] = df[['Postcode', 'Latitude', 'Longitude']].sample(n=NUM_RIDES, replace=True).reset_index(drop=True)
rides[['finish', 'finish_latitude', 'finish_longtitude']] = df[['Postcode', 'Latitude', 'Longitude']].sample(n=NUM_RIDES, replace=True).reset_index(drop=True)
rides['distance'] = [geodesic((x1, y1), (x2, y2)).km for x1, y1, x2, y2 in tqdm(zip(rides['start_latitude'], rides['start_longtitude'], rides['finish_latitude'], rides['finish_longtitude']), total=NUM_RIDES)]
                                                                            
start = pd.to_datetime('2010-01-01')
end = pd.to_datetime('2020-01-01')
rides['start_time'] = random_dates(start, end, NUM_RIDES)
rides['distance'] = rides['distance'].round(2)
rides['road_time'] = abs(np.random.normal(size=NUM_RIDES, scale=10)) + rides['distance'] * abs(np.random.normal(size=NUM_RIDES, loc=1, scale=0.25))
rides['road_time'] = rides['road_time'].astype('int')
rides['road_time'] = pd.to_timedelta(rides['road_time'], unit='m')
rides['finish_time'] = rides['start_time'] + rides['road_time']
rides['cost'] = [count_cost(s, d) for s, d in tqdm(zip(rides.start_time, rides.distance), total=NUM_RIDES)]
rides['cost'] = rides['cost'].round(2)
driver_rate_idx = np.random.randint(low=0, high=NUM_RIDES, size=int(NUM_RIDES*0.3))
driver_rate_distribution_arr = np.random.multinomial(1, [0.2, 0.05, 0.1, 0.25, 0.4], size=int(NUM_RIDES*0.3))
rides['driver_rate'][driver_rate_idx] = np.where(driver_rate_distribution_arr == 1)[1] + 1
driver_feedback_categories_good = ['great service', 'nice car', 'wonderful companion', 'neat and tidy', 'expert navigation', 'recommend']
driver_feedback_categories_bad = ['awful service', 'bad car', 'unpleasant companion', 'dirty', 'non-expert navigation', 'not recommend']
category_driver_good_feedback_idx = np.random.choice(rides[rides.driver_rate > 3].index, size=int(NUM_RIDES*0.3*0.2))
rides["category_driver_feedback"][category_driver_good_feedback_idx] = np.random.choice(driver_feedback_categories_good, size=int(NUM_RIDES*0.3*0.2))

category_driver_bad_feedback_idx = np.random.choice(rides[rides.driver_rate < 4].index, size=int(NUM_RIDES*0.3*0.2))
rides["category_driver_feedback"][category_driver_bad_feedback_idx] = np.random.choice(driver_feedback_categories_bad, size=int(NUM_RIDES * 0.3 * 0.2))
text_good_feedback_driver_length = np.random.randint(low=0, high=7, size=int(NUM_RIDES*0.3*0.2))
text_good_feedback_driver_sample = [random.sample(driver_feedback_categories_good, i) for i in text_good_feedback_driver_length]
rides['text_driver_feedback'][category_driver_good_feedback_idx] = text_good_feedback_driver_sample

text_bad_feedback_driver_length = np.random.randint(low=0, high=7, size=int(NUM_RIDES*0.3*0.2))
text_bad_feedback_driver_sample = [random.sample(driver_feedback_categories_bad, i) for i in text_bad_feedback_driver_length]
rides['text_driver_feedback'][category_driver_bad_feedback_idx] = text_bad_feedback_driver_sample
client_rate_idx = np.random.randint(low=0, high=NUM_RIDES, size=int(NUM_RIDES*0.5))
client_rate_distribution_arr = np.random.multinomial(1, [0.2, 0.05, 0.1, 0.25, 0.4], size=int(NUM_RIDES*0.5))
rides['client_rate'][client_rate_idx] = np.where(client_rate_distribution_arr == 1)[1] + 1
client_feedback_categories_good = ['polite', 'pleasant', 'quiet', 'neat and tidy', 'recommend']
client_feedback_categories_bad = ['unpolite', 'unpleasant', 'loud', 'dirty', 'not recommend']
category_client_good_feedback_idx = np.random.choice(rides[rides.client_rate > 3].index, size=int(NUM_RIDES*0.3*0.2))
rides["category_client_feedback"][category_client_good_feedback_idx] = np.random.choice(client_feedback_categories_good, size=int(NUM_RIDES*0.3*0.2))

category_client_bad_feedback_idx = np.random.choice(rides[rides.client_rate < 4].index, size=int(NUM_RIDES*0.3*0.2))
rides["category_client_feedback"][category_client_bad_feedback_idx] = np.random.choice(client_feedback_categories_bad, size=int(NUM_RIDES * 0.3 * 0.2))
text_good_feedback_client_length = np.random.randint(low=0, high=6, size=int(NUM_RIDES*0.3*0.2))
text_good_feedback_client_sample = [random.sample(client_feedback_categories_good, i) for i in text_good_feedback_client_length]
rides['text_client_feedback'][category_client_good_feedback_idx] = text_good_feedback_client_sample

text_bad_feedback_client_length = np.random.randint(low=0, high=6, size=int(NUM_RIDES*0.3*0.2))
text_bad_feedback_client_sample = [random.sample(client_feedback_categories_good, i) for i in text_bad_feedback_client_length]
rides['text_client_feedback'][category_client_good_feedback_idx] = text_bad_feedback_client_sample
rides.to_csv("rides.csv")