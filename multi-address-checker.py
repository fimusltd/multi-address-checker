#!/usr/bin/python

import fileinput
import re
import pybitcoin
from pybitcoin import BitcoinPrivateKey #pip install pybitcoin
from pybitcoin import BitcoinPublicKey #pip install pybitcoin
import requests #pip install -U requests[socks]
import re
import argparse
from tqdm import tqdm #pip install tqdm

args=""

def processArgs():
	global args
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--input','-i', action='store', dest='input', help='File to analyze')
	parser.add_argument('--output','-o', action='store', dest='output', help='File to save CSV with balances')
	parser.add_argument('--anonymous','-a', action='store_true', help="If this option is enabled, the program is executed via Tor Proxy in the port 9050")
	args=parser.parse_args()

def privateKeyToAddress(private_key):
	return BitcoinPrivateKey(private_key).public_key().address()

def checkBalance(address):
	global args
	if(args.anonymous):
		resp = requests.get('https://blockchain.info/es/q/addressbalance/' + address, 
			proxies=dict(http='socks5://localhost:9050',https='socks5://localhost:9050')).text
	else:
		resp = requests.get('https://blockchain.info/es/q/addressbalance/' + address).text
	if resp.isdigit():
		return int(resp)
	else:
		return 0

def main():
	global args
	addresses=[]
	private_keys=[]
	addresses_with_balance=[]
	private_keys_with_balance=[]

	#Print messages
	if(args.anonymous):
		print("Anonymous mode enalbed. Check that Tor Router is running.")

	#Find addresses and private keys inside STDIN
	print("Searching for bitcoin addresses...")
	print("")
	with open(args.input) as f:
		content = f.readlines()
	for line in content:

		#Find all bitcoin addresses
		for match in re.findall('[13][a-km-zA-HJ-NP-Z1-9]{25,34}',line):
			print("Match: " + match)
			addresses.append(match)

		#Find all bitcoin private keys
		for match in re.findall('[5KL][1-9A-HJ-NP-Za-km-z]{50,51}',line):
			print("Match: " + match)
			private_keys.append(match)
	print("")

	#Remove duplicate public addresses (that correspond to some private key)
	print("Removing duplicate addresses (private key match)...")
	print("")
	for private_key in private_keys:
		address=BitcoinPrivateKey(private_key).public_key().address()
		if address in addresses:
			print("Removed: " + address)
			addresses.remove(address)
	print("")

	#Get addressess with balance
	print("Getting address with balance...")
	print("")

	max_progress=len(addresses)+len(private_keys)
	with tqdm(total=max_progress,unit='check') as pbar:

		for address in addresses:
			balance=checkBalance(address)
			balance=float(balance)/float(100000000) #Convert satoshi to Bitcoin
			if balance>0:
				#print(address + " has " + str(balance) + " satoshi (" + str(float(balance)/float(100000000)) + " BTC)")
				with open(args.output, "a") as myfile:
					myfile.write(address + ",," + str(balance) + "\n")
				pass
			pbar.update(1)

		for private_key in private_keys:
			address=privateKeyToAddress(private_key)
			balance=checkBalance(address)
			balance=float(balance)/float(100000000) #Convert satoshi to Bitcoin
			if balance>0:
				#print(address + " " + str(balance) + " has " + str(balance) + " satoshi (" + str(float(balance)/float(100000000)) + " BTC)")
				with open(args.output, "a") as myfile:
					myfile.write(address + "," + private_key + "," + str(balance) + "\n")
				pass
			pbar.update(1)

	print("")



processArgs()
main()