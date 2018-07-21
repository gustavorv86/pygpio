#!/usr/bin/env python

'''
Created on 19 abr. 2018

@author: gustavorv86
'''

import os
import sys

PINOUT_OPI = [
	('PA0'  , '0'),
	('PA1'  , '1'),
	('PA2'  , '2'),
	('PA3'  , '3'),
	('PA4'  , '4'),
	('PA5'  , '5'),
	('PA6'  , '6'),
	('PA7'  , '7'),
	('PA8'  , '8'),
	('PA9'  , '9'),
	('PA10' , '10'),
	('PA11' , '11'),
	('PA12' , '12'),
	('PA13' , '13'),
	('PA14' , '14'),
	('PA18' , '18'),
	('PA19' , '19'),
	('PA20' , '20'),
	('PA21' , '21'),
	('PC0'  , '64'),
	('PC1'  , '65'),
	('PC2'  , '66'),
	('PC3'  , '67'),
	('PC4'  , '68'),
	('PC7'  , '71'),
	('PD14' , '110'),
	('PG6'  , '198'),
	('PG7'  , '199'),
	('PG8'  , '200'),
	('PG9'  , '201')
]

PINOUT_OPI_ZERO = [
	('PA0'  , '0'),
	('PA1'  , '1'),
	('PA2'  , '2'),
	('PA3'  , '3'),
	('PA6'  , '6'),
	('PA7'  , '7'),
	('PA10' , '10'),
	('PA11' , '11'),
	('PA12' , '12'),
	('PA13' , '13'),
	('PA14' , '14'),
	('PA15' , '15'),
	('PA16' , '16'),
	('PA18' , '18'),
	('PA19' , '19'),
	('PG6'  , '198'),
	('PG7'  , '199')
]

# Change Pinout board (PINOUT_OPI / PINOUT_OPI_ZERO)
PINOUT = PINOUT_OPI

VALUE_HIGH = '1'
VALUE_LOW  = '0'

MODE_IN  = 'in'
MODE_OUT = 'out'

DEFAULT_GPIO_PATH = '/sys/class/gpio/'



def pin_to_phy(pin) :
	for pin_tuple in PINOUT :
		if pin_tuple[0] == pin :
			return pin_tuple[1]   
	
	return None


def pin_export(phy) :
	fdesc = open(DEFAULT_GPIO_PATH + 'export', 'w')
	fdesc.write(phy)
	fdesc.close()


def pin_mode(pin, mode=MODE_OUT, value=VALUE_LOW) :
	phy = pin_to_phy(pin)
	if phy == None :
		print('ERROR: invalid pin')
		return False
	
	if not os.path.isdir(DEFAULT_GPIO_PATH + 'gpio' + phy) :
		pin_export(phy)

	try :
		fdesc = open(DEFAULT_GPIO_PATH + 'gpio' + phy + '/direction', 'w')
		fdesc.write(mode);
		fdesc.close()
		
		if mode == MODE_OUT :
			fdesc = open(DEFAULT_GPIO_PATH + 'gpio' + phy + '/value', 'w')
			fdesc.write(value)
			fdesc.close()
		
		return True
	
	except IOError :
		print('ERROR: invalid argument')
		return False



def pin_read(pin) :
	phy = pin_to_phy(pin)
	if phy == None :
		print('ERROR: invalid pin')
		return None
	
	if not os.path.isdir(DEFAULT_GPIO_PATH + 'gpio' + phy) :
		print('ERROR: unexport pin')
		return None
	
	fdesc = open(DEFAULT_GPIO_PATH + 'gpio' + phy + '/value', 'r')
	strvalue = fdesc.readline().strip()
	fdesc.close()
	
	try :
		value = int(strvalue)
	except ValueError :
		value = None
	return value



def pin_write(pin, value=VALUE_LOW) :
	phy = pin_to_phy(pin)
	if phy == None :
		print('ERROR: invalid pin')
		return False
	
	if not os.path.isdir(DEFAULT_GPIO_PATH + 'gpio' + phy) :
		print('ERROR: unexport pin')
		return False
	
	fdesc = open(DEFAULT_GPIO_PATH + 'gpio' + phy + '/value', 'w')
	fdesc.write(value)
	fdesc.close()
	
	return True


def pin_unexport(pin) :
	phy = pin_to_phy(pin)
	if phy == None :
		print('ERROR: invalid pin')
		return False
	
	if not os.path.isdir(DEFAULT_GPIO_PATH + 'gpio' + phy) :
		print('ERROR: unexport pin')
		return False
	
	fdesc = open(DEFAULT_GPIO_PATH + 'unexport', 'w')
	fdesc.write(phy)
	fdesc.close()
	
	return True
	

def gpio_readall() :
	print('PIN \t PHY \t MODE \t VALUE')
	print('============================================')
		
	for pin_tuple in PINOUT :
		strphy = str(pin_tuple[1])
		mode = 'none'
		value = ''
		if os.path.isdir(DEFAULT_GPIO_PATH + 'gpio' + strphy) :
			fdesc = open(DEFAULT_GPIO_PATH + 'gpio' + strphy + '/direction', 'r')
			mode = fdesc.readline().strip()
			fdesc.close()

			fdesc = open(DEFAULT_GPIO_PATH + 'gpio' + strphy + '/value', 'r')
			value = fdesc.readline().strip()
			fdesc.close()

		print(pin_tuple[0] + ' \t ' + strphy + ' \t ' + mode + ' \t ' + value)
		
	return


def gpio_help() :
	script_name = os.path.basename(__file__)
	
	print('USAGE: ')
	print(' \t ' + script_name + ' readall')
	print(' \t ' + script_name + ' in PXNN')
	print(' \t ' + script_name + ' out PXNN [0|1]')
	print(' \t ' + script_name + ' read PXNN')
	print(' \t ' + script_name + ' write PXNN [0|1]')
	print(' \t ' + script_name + ' close PXNN')
	print
	
	return
	
	
def gpio(argv) :
	argc = len(argv)
	
	option = 'help'
	pin = ''
	value = VALUE_LOW
	
	if argc >= 2 :
		option = sys.argv[1]
		
	if argc >= 3 :
		pin = sys.argv[2]
		
	if argc >= 4 :
		value = sys.argv[3]
		
	if option == 'help' or option == '--help' or option == '-h' or option == '?' :
		gpio_help()
	
	elif option == 'readall' :
		gpio_readall()
	
	elif option == 'in' :
		pin_mode(pin, MODE_IN, value)
	
	elif option == 'out' :
		pin_mode(pin, MODE_OUT, value)
		
	elif option == 'read' :
		value = pin_read(pin)
		if value != -1 :
			print(value)
		
	elif option == 'write' :
		pin_write(pin, value)
	
	elif option == 'close' :
		pin_unexport(pin)
	
	else :
		print('ERROR: invalid arguments')
	
	return
	
	
if __name__ == '__main__' :
	gpio(sys.argv)

