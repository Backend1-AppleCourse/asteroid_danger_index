
def create_graphs(json_variable, request_type):
    data = json.loads(json_variable)
    asteroids = data['near_earth_objects']
    min_diameters = []
    miss_distances = []
    for date in asteroids:
        for asteroid in asteroids[date]:
            if request_type == 1:
                min_diameters.append(float(asteroid['est_diameter_min'])/float(asteroid['relative_velocity'])) 
            else:
                miss_distances.append(float(asteroid['miss_distance'])/float(asteroid['est_diameter_max']))
    if request_type == 1:
        plt.plot(min_diameters)
        plt.title('min_diameter/velocity')
        plt.show()
    else:
        plt.plot(miss_distances)
        plt.title('miss_distance/max_diameter')
        plt.show()

def calculate_danger_index(A, B, C, asteroid):
    return A*(asteroid['est_diameter_min'] + asteroid['est_diameter_max'])/2 + B*float(asteroid['relative_velocity']) * 1/C*float(asteroid['miss_distance'])

def plot_danger_index(json_variable, A=1, B=1,C=1):
    data = json.loads(json_variable)
    asteroids = data['near_earth_objects']
    danger_indexes = []
    asteroid_names = []
    for date in asteroids:
        for asteroid in asteroids[date]:
            danger_indexes.append(calculate_danger_index(A,B,C,asteroid))
            asteroid_names.append(asteroid['name'])
    plt.plot(asteroid_names, danger_indexes)
    plt.show()