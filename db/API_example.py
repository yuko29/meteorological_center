from mongoDB import mongoDB

earthEqake_test = {'time': '2023-5-12 03:40:52', 'M_L': 3.6, 'focal_dep': 3.2, 'longitude': 41.0, 'latitude': 20.7, 'magnitude': [{'factory': '竹', 'magnitude': 0.00032644588703523386}, {'factory': '中', 'magnitude': 0.00019905740360289052}, {'factory': '南', 'magnitude': 0.0003714193582435097}]}
earthEqake_test2 = {'time': '2023-5-12 03:40:52', 'M_L': 3.6, 'focal_dep': 3.2, 'longitude': 41.0, 'latitude': 20.7, 'magnitude': [{'factory': '竹', 'magnitude': 0.00032644588703523386}, {'factory': '中', 'magnitude': 0.00019905740360289052}, {'factory': '南', 'magnitude': 0.0003714193582435097}]}
electricity_test = {'region':"北", 'power_usage':512.3, 'power_generate': 482.1, 'time': "2023-5-12 03:40:52"}
electricity_test2 = {'region':"南", 'power_usage':510.3, 'power_generate': 472.1, 'time': "2023-5-12 03:40:52"}
reservoir_test = {'time':"2023-5-12 03:40:52", 'percentage': 427.6, 'water_supply': 321.2, 'name': "德基水庫"}
reservoir_test2 = {'time':"2023-5-12 03:40:52", 'percentage': 42.6, 'water_supply': 321.2, 'name': "德基水庫"}
earthEqake_test_list = []

for i in range(10):
    earthEqake_test_list.append(earthEqake_test)


a = mongoDB()
# a.exampleAPI()
# a.exampleAPI2()


a.insertEarthquake(earthEqake_test)
a.insertEarthquake(earthEqake_test2)
a.insertEarthquake(earthEqake_test_list)
a.insertElectricity(electricity_test)
a.insertElectricity(electricity_test2)
a.insertReservoir(reservoir_test)
a.insertReservoir(reservoir_test2)

print(f"RETRIEVING RESERVOIR...")
print(a.retrieveReservoir(50, "德基水庫"))
for i in a.retrieveReservoir(50, "2"):
    print(i)

print(f"\n\n\nRETRIEVING ELECTRICITY...\n\n")

for i in a.retrieveElectricity(52, "北"):
    print(i)

print(f"\n\n\nRETRIEVING EARTHQUAKE...\n\n")
print(list(a.retrieveEarthquake(52)))
for i in a.retrieveEarthquake(52):
    print(i)

print(f"\n\n\nRETRIEVING EARTHQUAKE FOR FACTORY...\n\n")

for i in a.retrieveFactoryEarthquake(factory = "竹"):
    print(i)

a.reset()

# a.delete