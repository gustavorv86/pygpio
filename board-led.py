#!/usr/bin/env python

'''
Created on 19 abr. 2018

@author: gustavorv86
'''

import os
import sys


DEFAULT_LED_PATH = '/sys/class/leds/'


LED_GREEN_PATHS = [
	DEFAULT_LED_PATH + 'orangepi:green:pwr/brightness',
	DEFAULT_LED_PATH + 'green_led/brightness'
]

LED_RED_PATHS = [
	DEFAULT_LED_PATH + 'orangepi:red:status/brightness',
	DEFAULT_LED_PATH + 'red_led/brightness'
]

LED_GREEN = 'green'
LED_RED = 'red'

VALUE_HIGH = '1'
VALUE_LOW  = '0'


def _get_path(led) :
	led_paths = None
	if led == LED_GREEN :
		led_paths = LED_GREEN_PATHS
	elif led == LED_RED :
		led_paths = LED_RED_PATHS
	else :
		return None
	
	led_path = None
	for path in led_paths :
		if os.path.isfile(path) :
			led_path = path
			break
		
	return led_path


def get_value(led) :
	led_path = _get_path(led)
	if led_path == None :
		print('ERROR: device not found')
		return None
	
	fd = open(led_path, 'r')
	strvalue = fd.readline().strip()
	fd.close()
	return int(strvalue)


def set_value(led, value=VALUE_LOW) :
	led_path = _get_path(led)
	if led_path == None :
		print('ERROR: device not found')
		return False
	
	fd = open(led_path, 'w')
	fd.write(value)
	fd.close()
	return True


def board_led_help() :
	script_name = os.path.basename(__file__)
	
	print('USAGE: ')
	print(' \t ' + script_name + ' [read|write] [red|green] [0|1]')
	print(' \t ' + script_name + ' [help|--help|-h|?]')
	print
	
	return


def board_led(argv) :
	argc = len(argv)
	
	option = 'help'
	led = None
	value = VALUE_LOW
	
	if argc >= 2 :
		option = argv[1]
		
	if argc >= 3 :
		led = argv[2]
		
	if argc >= 4 :
		value = argv[3]
		
	if option == 'help' or option == '--help' or option == '-h' or option == '?' :
		board_led_help()
		return

	if led == None :
		print('ERROR: invalid arguments')
		return
	
	if option == 'read' :
		value = get_value(led)
		if value != None :
			print(value)
	
	elif option == 'write' :
		set_value(led, value)
	
	else :
		print('ERROR: invalid arguments')
	
	return
		

if __name__ == '__main__' :
	board_led(sys.argv)
		
		
		
