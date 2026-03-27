import math
import random

COST_PER_KM = 15
DAYS_PER_YEAR = 300

def haversine(c1, c2):
    R = 6371
    lat1, lon1 = c1
    lat2, lon2 = c2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

def generate_nodes(n=12):
    return [{"id": i, "coord": (random.uniform(19.0,20.0), random.uniform(-99.5,-98.5))} for i in range(n)]

def route_distance(route):
    return sum(haversine(route[i]["coord"], route[i+1]["coord"]) for i in range(len(route)-1))

def nearest_neighbor(nodes):
    unvisited = nodes[:]
    route = [unvisited.pop(0)]
    while unvisited:
        last = route[-1]
        nxt = min(unvisited, key=lambda x: haversine(last["coord"], x["coord"]))
        route.append(nxt)
        unvisited.remove(nxt)
    return route

def two_opt(route):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route)-2):
            for j in range(i+1, len(route)):
                if j-i == 1:
                    continue
                new_route = route[:]
                new_route[i:j] = route[j-1:i-1:-1]
                if route_distance(new_route) < route_distance(best):
                    best = new_route
                    improved = True
        route = best
    return best

def main():
    nodes = generate_nodes()
    nn = nearest_neighbor(nodes)
    opt = two_opt(nn)

    d1 = route_distance(nn)
    d2 = route_distance(opt)

    savings_km = d1 - d2
    savings_daily = savings_km * COST_PER_KM
    savings_annual = savings_daily * DAYS_PER_YEAR

    print("Baseline distance:", round(d1,2))
    print("Optimized distance:", round(d2,2))
    print("Distance reduction:", round(savings_km,2))
    print("Annual savings (MXN):", round(savings_annual,2))

if __name__ == "__main__":
    main()
