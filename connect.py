from mongoDB import mongoDB

earthEqake_test = {'time':"2023-5-12 03:40:52", 'M_L':3.6, 'focal_dep': 3.2, 'longitude': 41.0, 'latitude': 20.7}
electricity_test = {'region':"北", 'power_usage':512.3, 'power_generate': 482.1, 'time': "2023-5-12 03:40:52"}
electricity_test2 = {'region':"南", 'power_usage':512.3, 'power_generate': 482.1, 'time': "2023-5-12 03:40:52"}
reservoir_test = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "德基水庫"}
reservoir_test2 = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "石門水庫"}


a = mongoDB()
# a.exampleAPI()
# a.exampleAPI2()


# a.insertEarthquake(earthEqake_test)
# a.insertElectricity(electricity_test)
# a.insertElectricity(electricity_test2)
# a.insertReservoir(reservoir_test)
# a.insertReservoir(reservoir_test2)

# for i in a.retrieveReservoir(50, "德基水庫"):
#     print(i)

# for i in a.retrieveElectricity(52, "北"):
#     print(i)

# for i in a.retrieveEarthquake(52):
#     print(i)

a.reset()

# a.delete