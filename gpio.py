# -*- coding: iso-8859-1 -*-
import logging
import RPi.GPIO as GPIO
from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException, MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")

class Gpio(NeuronModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # the args from the neuron configuration
        self.set_pin_high = kwargs.get('set_pin_high', None)
        self.set_pin_low = kwargs.get('set_pin_low', None)       
        self.sensor = kwargs.get('sensor', None)
        self.fahrenheit = kwargs.get('fahrenheit', False)
        self.one_decimal_place = kwargs.get('one_decimal_place', False)
        self.GPIO = GPIO

        # check if parameters have been provided
        if self._is_parameters_ok():
            # set gpio pins to high or low 
            self.GPIO.setwarnings(False)
            self.GPIO.setmode(GPIO.BCM)

            if self.set_pin_high:
                self.GPIO.setup(self.set_pin_high, GPIO.OUT)
                self.GPIO.output(self.set_pin_high, GPIO.HIGH)
                logger.debug('[GPIO] Set pin %s to high' % self.set_pin_high)
                
            if self.set_pin_low:
                self.GPIO.setup(self.set_pin_low, GPIO.OUT)                
                self.GPIO.output(self.set_pin_low, GPIO.LOW)              
                logger.debug('[GPIO] Set pin %s to low' % self.set_pin_low)
                
            # 1-Wire 
            if self.sensor:
                def callsensor():
                    with open("/sys/bus/w1/devices/" + self.sensor + "/w1_slave", 'r') as f:	  
                        lines = f.read().splitlines()	
                        
                    temp_line = lines[1].find('t=')	
                    temp_output = lines[1].strip()[temp_line+2:] 
                    temp_celsius = float(temp_output) / 1000
                    
                    if self.fahrenheit:
                        temp_fahrenheit = temp_celsius * 9.0 / 5.0 + 32.0
                        logger.debug('[GPIO] Sensor %s returns %s° fahrenheit' % (self.sensor, '%.1f' % float(temp_fahrenheit)))
                        return temp_fahrenheit
                    else:
                        logger.debug('[GPIO] Sensor %s returns %s° celsius' % (self.sensor, '%.1f' % float(temp_celsius)))
                        return temp_celsius		
                
                if self.one_decimal_place:
                    message = {"sensor": str('%.1f' % float(callsensor())).rstrip('0').rstrip('.')}
                else:
                    message = {"sensor": str(round(callsensor())).rstrip('0').rstrip('.')}
                
                self.say(message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException, MissingParameterException
        """

        def check_for_integer(parameter):
            if isinstance(parameter, list):     
                for item in parameter:   
                    if isinstance(item, (int)):
                        continue
                    else:
                        raise InvalidParameterException("[Gpio] %s List contains not valid integers" % parameter)       
            else:
                try:
                    parameter = int(parameter)
                except ValueError:   
                    raise InvalidParameterException("[Gpio] %s is not a valid integer" % parameter)

        if self.set_pin_high:
            check_for_integer(self.set_pin_high)
            
        elif self.set_pin_low:
            check_for_integer(self.set_pin_low)

        elif self.sensor:
            try:
                with open("/sys/bus/w1/devices/" + self.sensor + "/w1_slave", 'r') as f:   
                    lines = f.read().splitlines()   
            except IOError:
                raise MissingParameterException("[Gpio] Sensor %s not found" % self.sensor)

        elif self.fahrenheit and not self.sensor:
            raise MissingParameterException("[Gpio] You must set a sensor")
        
        elif self.one_decimal_place and not self.sensor:
            raise MissingParameterException("[Gpio] You must set a sensor")
        
        else:
            raise MissingParameterException("[Gpio] You musst set at least one GPIO pin or sensor")
        return True
