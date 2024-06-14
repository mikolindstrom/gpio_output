# Gpio
Gpio neuron for kalliope
## Synopsis

Switch a gpios between high and low and get temperaturs or other data from the 1-wire bus.

## Installation
```bash
kalliope install --git-url https://github.com/corus87/gpio-neuron
```

## Options

| Parameter        | Required | Choice  | Default | Comment                  |
|------------------|----------|---------|---------|--------------------------|
| set_pin_high     | no       | integer |         | GPIO numbers (BCM)       |
| set_pin_low      | no       | integer |         |                          |
| sensor           | no       | string  |         | (GPIO_GCLK) GPIO 4       |
| fahrenheit       | no       | boolean | False   | Default is celsius       |
| one_decimal_place| no       | boolean | False   | Default no decimal place |

## Return values

| Name         | Description                                      | Type   | Sample |
|--------------|--------------------------------------------------|--------|--------|
| sensor       | Returns the temperature in celsius or fahrenheit | string | 24     |


## Synapses example
```
  - name: "temp-out-living"
    signals:
      - order: "what are the temperaturs"
    neurons:
      - gpio:
          sensor: "28-0416b37f9bff"          
          say_template:
              - "outside {{ sensor }} degree,"   
      - gpio:        
          sensor: "28-0316b3bd7bff"
          say_template:
              - "and in the living room {{ sensor }} degree."  
  
  - name: "all-lights-on"
    signals:
      - order: "Turn all lights on"
    neurons:
      - gpio:
          set_pin_high:
            - 17
            - 18
            - 22
            - 27
 
 - name: "table-lamp-off"
    signals:
      - order: "Turn table lamp off"
    neurons:
      - gpio:
          set_pin_low: 17
```
## Notes
To get the sensor ID of each sensor use:
> cat /sys/devices/w1_bus_master1/w1_master_slaves



