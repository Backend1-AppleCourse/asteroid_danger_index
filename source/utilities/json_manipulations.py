
def filter_response(response):
    data = json.loads(response)

    asteroids = data['near_earth_objects']
    filtered_asteroids = []
    for date in asteroids:
        filtered_date = []
        for asteroid in asteroids[date]:
            filtered_date.append({
                "id": asteroid['id'],
                "name": asteroid['name'],
                "est_diameter_min": asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'],
                "est_diameter_max": asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'],
                "miss_distance": asteroid['close_approach_data'][0]['miss_distance']['kilometers'],
                "relative_velocity": asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']
            })
       
        filtered_asteroids.append( {date: filtered_date})
        asteroids[date] = filtered_date

    data['near_earth_objects'] = asteroids

    # json_data = json.dumps(filtered_asteroids)

    return json.dumps(data)