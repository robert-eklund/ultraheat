# Ultraheat

Script to read information from Landis+Gyr Ultraheat (T550)

With this script you can read a telegram from a Landis&Gyr Ultraheat T550 that is used by district heating companies, such as 'Tekniska Verken' in Linköping.

## Installation and usage:
This script uses a optical probe (IEC 62056-21) on an USB port to read the telegrams from the meter.

## Configuration - Docker Compose

### Docker compose
This Docker image will send the values to Home Assistant in kW, using MQTT.

Make sure to update ULTRAHEAT_MQTT_BROKER and ULTRAHEAT_USB_DEVICE

    version: "2.1"
    services:
      ultraheat:
        image: thintux/ultraheat:v1
        container_name: ultraheat
        privileged: true
        restart: unless-stopped
        environment:
          - ULTRAHEAT_MQTT_BROKER=192.168.68.121
          - ULTRAHEAT_USB_DEVICE=/dev/ttyUSB0
        volumes:
          - /etc/localtime:/etc/localtime:ro
          - /dev/:/dev/

### Home Assistant

    sensor:
      - platform: mqtt
        state_topic: "ultraheat/district_heating_meter"
        unit_of_measurement: "kWh"
        name: district_heating_meter_total
            value_template: '{{ value_json["total_kwh"] }}'

    utility_meter:
      district_heating_hourly:
        source: sensor.district_heating_meter_total
        cycle: hourly
      district_heating_daily:
        source: sensor.district_heating_meter_total
        cycle: daily
      district_heating_weekly:
        source: sensor.district_heating_meter_total
        cycle: weekly
      district_heating_monthly:
        source: sensor.district_heating_meter_total
        cycle: monthly
      district_heating_yearly:
        source: sensor.district_heating_meter_total
        cycle: yearly

## Note:
My meter is connected to 220V so I read every minute.
If your meter is battery powered, then you should read much more seldom to avoid
draining the battery.

## Requirements:
- An optical probe (IEC 62056-21 standard) to place on the meter, for example: https://www.amazon.de/dp/B01B8N0ASY/ref=pe_3044161_185740101_TE_item
- Docker
- Home Assistant

