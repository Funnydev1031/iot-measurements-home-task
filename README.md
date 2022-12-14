# Mollybet Frontend Take-Home

IoT devices are getting more wide spread by the day, controlling everything from heating to door locks to baby monitors.

We would like you to create an interface that displays data streamed over a WebSocket by IoT devices. A simple interface might be a table format like below, but you are welcome to flex your design muscles and display the data as a dashboard or in some other format so long as it meets the requirements described in the 'What we are looking for' section. We estimate that this task should take you 1 to 2 hours.

| Location   | Metric                   | Tags                           | Device               | Value                 | Timestamp                 |
| ---------- | ------------------------ | ------------------------------ | -------------------- | --------------------- | ------------------------- |
| Location 1 | Metric 1<br/>Metric 2    | Tag, Tag ...<br />Tag, Tag ... | Device<br/>Device    | Value<br/>Value       | Timestamp<br/>Timestamp   |
| ...                                                                                                                                               |

To do this we have provided a backend which has `GET` endpoints to retrieve information about the devices, metrics and locations. These can be seen documented on `http://localhost:65000/docs` (once you have started the `docker-compose` instance). 

Devices have the properties:
- `id`
- `location_id` (which should match the id from the location response)
- `mac` (which should match the mac address in the websocket message)

Metrics have the properties: 
- `id`
- `name` (which should match the metric name in the websocket message)
- `unit`

Locations have the properties:
- `id`
- `name`

In addition to these endpoints there is a websocket at `ws://localhost:65000/measurements/ws` which sends live measurement updates in one of three formats:

- `["MEASUREMENT", <device_mac_address>, <metric_name>, <value>, <list of tags>]`, a measurement from a device.
- `["PING", <device_mac_address>]`, a ping from the device (device is still alive but has no update to send).
- `["ERROR", <device_mac_address>, <error message>]`, an error occured on the device.

## Running the  stack

This tech stack was created using docker and docker-compose, so you will need docker and docker-compose installed (https://docs.docker.com/compose/install/). You can check if you have installed using `docker-compose version` which should show you your version information if you have it installed correctly:

```
mollybet-frontend-takehome => docker-compose version
docker-compose version 1.29.2, build 5becea4c
docker-py version: 5.0.0
CPython version: 3.7.10
OpenSSL version: OpenSSL 1.1.0l  10 Sep 2019
```

With docker-compose installed and inside the top level directory, should be able to run:
1. `docker-compose build`, to initially build the images
2. `docker-compose up`, to run both the backend and frontend

(or just do both at the same time with `docker-compose build && docker-compose up`)

When this is running, you should be able to access the backend on `http://localhost:65000` and the frontend on `http://localhost:65001`. Both should automatically rebuild when you save (but you will have have to reload the page to see them in your browser). You should be able to do this task only editing the files inside `frontend/src`, however if you are welcome to change other files if you like.

You can add additional packages using `npm install ...` but you will have to re-run the above commands for them to work in the build.

## What we are looking for

- A clean interface that clearly displays the most relevant information but also enables you to see detailed/meta information should a user want to.
- A logical and performant handling of state data, there are only 4 devices in this take-home but you could imagine there being hundreds or even thousands.
- The ability to both sort and filter the data if the user wishes to see a particular set of information.
- Modern react and javascript practices including strong typing with typescript and functional components using hooks. 

## What would be nice to see

- An eye for design.
- Good file management and separation of concerns.
- Easy to read and highly maintainable code.

## Helpful hints

- Devices can report multiple different metrics.
- Multiple devices can report the same metric as they are in different locations.
- Tags are to help a user with filtering the measurements.
- There are some booby-traps that we would like see you handle cleanly and keep the user aware of relevant information.

## When you are done

Once you have finished, if you could zip your solution (the whole iot-measurements folder, preferably delete node_modules before doing so) and send it back to us so we can review your code.