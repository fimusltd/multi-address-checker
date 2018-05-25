#!/user/bin/python
import fileinput
import re
from pybitcoin import BitcoinPrivateKey #pip install pybitcoin

def main():
	adresses=[]
	private_keys=[]

	#Find addresses and private keys inside STDIN
	for line in fileinput.input():

		#Find all bitcoin addresses
		print("Searching for Bitcoin addresses...")
		for match in re.findall('^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',line):
			addresses.append(match)

		#Find all bitcoin private keys
		print("Searching for Bitcoin private keys...")
		for match in re.findall('^[5KL][1-9A-HJ-NP-Za-km-z]{50,51}$',line):
			private keys.append(match)

	#Remove duplicate public addresses (that correspond to some private key)
	





main()