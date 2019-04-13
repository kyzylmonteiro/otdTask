stopsFile = open("stops.txt", "r");
stop_id_list1=list()
stop_code_list1=list()
stop_name_list1=list()
stop_lat_list1=list()
stop_lon_list1=list()
for line in stopsFile:
	line=line[:-1] # removing \n
	# print(line)
	if(line.find('"')==-1):
		# print(line.split(","))
		stop_id,stop_code,stop_name,stop_lat,stop_lon=line.split(",")
	else:
		stop_id,stop_code,stop_name1,stop_name2,stop_lat,stop_lon=line.split(",")
		stop_name=stop_name1[1:]+stop_name2[:-1] #removing quotes
	stop_id_list1.append(stop_id);
	stop_code_list1.append(stop_code);
	stop_name_list1.append(stop_name);
	stop_lat_list1.append(stop_lat);
	stop_lon_list1.append(stop_lon);

stopsFile.close()

stopTimesFile = open("stop_times.txt", "r");
trip_id_list2=list()
arrival_time_list2=list()
departure_time_list2=list()
stop_id_list2=list()
stop_sequence_list2=list()
for line in stopTimesFile:
	# print(line)
	trip_id,arrival_time,departure_time,stop_id,stop_sequence=line.split(",")
	trip_id_list2.append(trip_id)
	arrival_time_list2.append(arrival_time)
	departure_time_list2.append(departure_time)
	stop_id_list2.append(stop_id)
	stop_sequence_list2.append(stop_sequence)

stopTimesFile.close()


tripsFile = open("trips.txt", "r");
route_id_list3=list()
service_id_list3=list()
trip_id_list3=list()
for line in tripsFile:
	# print(line)
	route_id,service_id,trip_id=line.split(",")
	route_id_list3.append(route_id)
	service_id_list3.append(service_id)
	trip_id_list3.append(trip_id[:-1])

tripsFile.close()

def findStopId(stop_name_given):
	try:
		return stop_id_list1[stop_name_list1.index(stop_name_given)]
	except :
		print("Invalid Name: "+stop_name_given)

def findTripId(stop_id_given):
	trips=list()
	try:
		for i in range(len(stop_id_list2)):
			if(stop_id_list2[i]==stop_id_given):
				trips.append(trip_id_list2[i])
	except:
		print("Error finding trips for: "+stop_id_given)
	return trips;

def findRouteId(trips_given):
	routes=list()
	try:
		# print(trip_id_list3)
		for t1 in range(len(trips_given)):
			for t in range(len(trip_id_list3)):
				if trips_given[t1]==trip_id_list3[t]:
					if(not(route_id_list3[t] in routes)):
						routes.append(route_id_list3[t])
	except:
		print("Error finding routes ")
	return routes;

def checkIfZeroHop(routes_given1,routes_given2):
	for route in routes_given1:
		if route in routes_given2:
			return True
		else:
			return False

# sourceName='Shankar Vihar / National Highway 8'
# destName='Matiyala Xing'
sourceName=input("sourceName:")
destName=input("destName:")

def mapAllStopsToRoutes():
	stopsInRoute=dict()
	uniqueRoutes=set()
	uniqueRoutes.update(route_id_list3);
	for route in uniqueRoutes:
		stops=list()
		try:
			trip=trip_id_list3[route_id_list3.index(route)]
			for t in range(len(trip_id_list2)):
				if trip_id_list2[t]==trip:
					if(not(stop_id_list2[t] in stops)):
						stops.append(stop_id_list2[t])
		except e:
			print(e)
		stopsInRoute[route]=stops
	return stopsInRoute
		


# ****0 hops****
sourceId=findStopId(sourceName)
destId=findStopId(destName)
sourceTrips=findTripId(sourceId)
destTrips=findTripId(destId)
sourceRoutes=findRouteId(sourceTrips)
destRoutes=findRouteId(destTrips)
isZeroHop=checkIfZeroHop(sourceRoutes,destRoutes)
print("Is Zero Hop?"+str(isZeroHop))

if isZeroHop==True:
	print("Zero Hops using routes with ids:")
	for route in sourceRoutes:
		if route in destRoutes:
			print(route)	

# ****1hop****
if isZeroHop==False:
	stopsInRoute=mapAllStopsToRoutes();

	# finds stops accesible from source and dest
	stopsAccessibleFromSource=list()
	stopsAccessibleFromDest=list()
	for route in sourceRoutes:
		# print(route+" "+str(len(stopsInRoute[route])))
		stopsAccessibleFromSource.extend(stopsInRoute[route])
	for route in destRoutes:
		# print(route+" "+str(len(stopsInRoute[route])))
		stopsAccessibleFromDest.extend(stopsInRoute[route])

	# checks if one hop
	isOneHop=False;
	interchangableStops=list()
	firstRoute=None
	secondRoute=None
	for stop in stopsAccessibleFromSource:
		if stop in stopsAccessibleFromDest:
			interchangableStops.append(stop);
			isOneHop=True;

	print("Is One Hop?"+str(isOneHop))
	# finds and prints routes in one hop 
	if isOneHop==True:
		for interchangeStop in interchangableStops:
			for route in sourceRoutes:
				if interchangeStop in stopsInRoute[route]:
					firstRoute=route;

			for route in destRoutes:
				if interchangeStop in stopsInRoute[route]:
					secondRoute=route;

			print("firstRoute:"+ firstRoute+ " Interchange at:"+ interchangeStop+" secondRoute:"+secondRoute)

	else:
		print("No 0 hop or 1 hop routes")

# print(sourceName,sourceId,sourceTrips,sourceRoutes,source0hopStops)
# print(destName,destId,destTrips,destRoutes,dest0hopStops)

