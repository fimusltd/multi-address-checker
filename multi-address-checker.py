#!/user/bin/python
import fileinput
import re
import pybitcoin
from pybitcoin import BitcoinPrivateKey #pip install pybitcoin
from pybitcoin import BitcoinPublicKey #pip install pybitcoin
import requests #pip install -U requests[socks]
import re

def main():
	addresses=[]
	private_keys=[]
	addresses_with_balance=[]
	private_keys_with_balance=[]

	#Find addresses and private keys inside STDIN
	print("Searching for bitcoin addresses...")
	print("")
	for line in fileinput.input():

		#Find all bitcoin addresses
		for match in re.findall('[13][a-km-zA-HJ-NP-Z1-9]{25,34}',line):
			print("Match: " + match)
			addresses.append(match)

		#Find all bitcoin private keys
		for match in re.findall('[5KL][1-9A-HJ-NP-Za-km-z]{50,51}',line):
			print("Match: " + match)
			private_keys.append(match)
	print("")

	print("Removing duplicate addresses (private key match)...")
	print("")
	#Remove duplicate public addresses (that correspond to some private key)
	for private_key in private_keys:
		address=BitcoinPrivateKey(private_key).public_key().address()
		if address in addresses:
			print("Removed: " + address)
			addresses.remove(address)
	print("")
	

def checkBalance(address):
	#Check if private key, convert to public key



main()