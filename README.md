# pyrkowy-gtfs-rt

A compact but quite intresting Python program for working with **GTFS** (General Transit Feed Specification) and **GTFS-RT** (Realtime) data from Poznań public transit operators. These same feeds power popular journey-planning apps like *jakdojade.pl* or *czynaczas.pl*.

This repo is intended as a building block for a future multi-city transit add-on to another of my projects, [SimpleDiscordBot](https://github.com/keciaM/SimpleDiscordBot-WebhookManager).

## Key Features (so far)

- **GTFS and GTFS-RT**  
  Downloading and analyzing both static timetables and realtime updates for all operators covered by the ZTM Poznań system (vehicles, delays, routes).
  *Currently supports only ZTM Poznań, but Kraków and GZM are next in line for integration.*

- **Vehicle lookup**  
  Query by vehicle number (fleet ID) to retrieve current GPS coordinates, status, and delay information. Also generates a 512×256 pixel map image showing the vehicle’s location using a StaticMap library.

- **Stop timetable with delays**  
  For any stop name or ID, returns upcoming departures along with realtime delay estimates.
