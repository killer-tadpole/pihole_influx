#! /usr/bin/python

# Script originally created by JON HAYWARD: https://fattylewis.com/Graphing-pi-hole-stats/
# Adapted to work with InfluxDB by /u/tollsjo in December 2016
# Updated by Cludch December 2016

# To install and run the script as a service under SystemD. See: https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux

import requests
import time
import uptime
from influxdb import InfluxDBClient

HOSTNAME = "home" # Pi-hole hostname to report in InfluxDB for each measurement
PIHOLE_API = "http://pihole.home/admin/api.php"
INFLUXDB_SERVER = "rpi3" # IP or hostname to InfluxDB server
INFLUXDB_PORT = 8086 # Port on InfluxDB server
INFLUXDB_USERNAME = "root"
INFLUXDB_PASSWORD = "password"
INFLUXDB_DATABASE = "home"
DELAY = 60 # seconds


def send_msg(domains_being_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today):
   json_body = [
       {
           "measurement": "pihole." + HOSTNAME.replace(".", "_"),
           "tags": {
              "host": HOSTNAME
           },
           "fields": {
              "domains_being_blocked": int(domains_being_blocked),
              "dns_queries_today": int(dns_queries_today),
              "ads_percentage_today": float(ads_percentage_today),
              "ads_blocked_today": int(ads_blocked_today),
              "uptime": int(uptime.uptime())
           }
       }
    ]
   print(json_body)
   # InfluxDB host, InfluxDB port, Username, Password, database
   client = InfluxDBClient(INFLUXDB_SERVER, INFLUXDB_PORT, INFLUXDB_USERNAME, INFLUXDB_PASSWORD, INFLUXDB_DATABASE) 

   # Uncomment to create the database (expected to exist prior to feeding it data)
   # client.create_database(INFLUXDB_DATABASE) 

   client.write_points(json_body)
   print(json_body)

if __name__ == '__main__':
        while True:
          #time.sleep(DELAY)
          api = requests.get(PIHOLE_API) # URI to pihole server api
          API_out = api.json()
          domains_being_blocked = (API_out['domains_being_blocked'])
          dns_queries_today = (API_out['dns_queries_today'])
          ads_percentage_today = (API_out['ads_percentage_today'])
          ads_blocked_today = (API_out['ads_blocked_today'])
          # print(domains_being_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today)

          send_msg(domains_being_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today)
          time.sleep(DELAY)
