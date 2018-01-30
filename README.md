#microbus

A bus transports passengers (data) across a route. A route consists of 2 or more stops.
In each stop, passengers unboard, and then waiting passengers board the bus.

## Installation

```bash
pip install microbus
```

## Usage

### BusStop

Passengers wait at a bus stop. When a bus reaches the stop, passengers on the bus will exit, arriving at the stop.
Passengers already waiting at stop will then board the bus.

A stop can have a callback for handling arriving passengers, and a callback, triggered once there are passengers waiting for the bus.

```python
stop = BusStop(
    arriving_passengers_handler=lambda stop, passengers: None,
    waiting_passengers_callback=lambda stop: None
)
stop.wait_for_bus([1,2,3])
```

### BusRoute

A BusRoute typically consists of 2 or more stops. A bus traversing a route will transit at each stop in order.
except for the first and last stop, for each intermediate stop it will drop boarded passengers then board new ones.
For the first stop, it will only board waiting passengers, and for the last stop it will only unboard passengers.

```python
stop1 = BusStop()
stop2 = BusStop()
stop3 = BusStop()
route = BusRoute((stop1, stop2, stop3))
```

### Bus

A Bus is what traverses a BusRoute, where once departed, it should transit at each stop and behave as described
above (see BusRoute).

A Bus cannot depart 2 routes at the same time. It has to either complete departing the route or cancel its trip
before departing a new route.

Once a bus departs, the actual control is given back to the invoker in form of generator, where each call to ```next```
will traverse to next stop, and ```close``` will cancel the trip

```python

bus = Bus()
trip = bus.depart(route)
curr_stop, remaining_route = next(trip)
curr_stop, remaining_route = next(trip)
```
You can continue doing so until it raises StopIteration exception which you'll have to handle

```python
try:
    next(trip)
    next(trip)
except StopIteration:
    '''route ended'''
```

or by manually checking the remaining route length

```python
_, remaining = next(trip)
if len(remaining): _, remaining = next(trip)
if len(remaining): _, remaining = next(trip)
```
or simply by iterating:
```python
for stop, remaining_route in bus.depart(route):
    print("Arrived at stop %s, remaining route: %s" % (stop, remaining_route))
```
you can cancel a trip midway by calling ```trip.close()```
```python
trip = bus.depart(route)
next(trip)
trip.close()
bus.depart(route2)
```

You must either finish a started trip, or cancel (close) it before attempting to depart a new route, otherwise
you get a ```SimultaneousRoutesException```


### Schedulers

#### BusScheduler

Through a ```BusScheduler``` you can schedule multiple routes for a bus as you wish. The scheduler will
take care of completing a scheduled route and jump to next scheduled one if/when scheduled.

```python
scheduler = BusScheduler(bus)
scheduler.schedule(route1)
scheduler.schedule(route2)
scheduler.run()
```

Running a scheduler will block the invoking thread, therefore it might make sense
to run it in background. Of course this depends on your use case, for example whether you have an existing event loop.

```python
import threading
scheduler = BusScheduler(bus)
threading.Thread(target=scheduler.run).start()
scheduler.schedule(route1)
scheduler.schedule(route2)
scheduler.schedule(route3)
```

#### DisjointRoutesBusScheduler

A ```DisjointRoutesBusScheduler``` has a similar API to BusScheduler. The only difference is that disjoint scheduler
will not schedule routes that are either:
- Already scheduled and not departed
- A subset of the route the bus is currently traversing, where the bus hasn't reached yet the first stop of that subset.