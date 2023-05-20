from mongoDB import mongoDB

earthEqake_test = {'time':"2023-5-12 03:40:52", 'M_L':3.6, 'focal_dep': 3.2, 'longitude': 41.0, 'latitude': 20.7}
electricity_test = {'region':"北", 'power_usage':512.3, 'power_generate': 482.1, 'time': "2023-5-12 03:40:52"}
reservoir_test = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "德基水庫"}


a = mongoDB()
a.exampleAPI()
a.exampleAPI2()
a.insertEarthquake(earthEqake_test)
a.insertElectricity(electricity_test)
a.insertReservoir(reservoir_test)