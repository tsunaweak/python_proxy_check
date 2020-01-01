#!/usr/bin/python3
import requests
import sys
import os

class ProxyChecker:
	url = 'https://ipv4.icanhazip.com' # This url is where send request to view ip address of the request
	proxyCount = 0
	goodProxy = 0
	def main(self):
		#This block use to parse the text file and send to to check_proxy function
		if len(sys.argv) > 1:
			file = open(sys.argv[1], "r").readlines()
			self.proxyCount = sum(1 for line in open(sys.argv[1]))
			if(self.proxyCount > 0):
				print("Number of proxy to check: {}".format(self.proxyCount))
				for proxy in file:
					data = proxy.strip('\n').split(':')
					self.check_proxy(data[0], data[1])
				print("Checking Proxy Complete.")
				print("Total Number: {}".format(self.proxyCount))
				print("Good Proxy: {}".format(self.goodProxy))
				print("Bad Proxy: {}".format(self.proxyCount - self.goodProxy))
			else:
				print("Selected text file cannot be empty")
		else:
			print("Command: ./proxy_checker proxylist.txt")
	def check_proxy(self, ip, port):
		#This block accept ip and port and determine what type of proxy it is,
		#then send it to send send_req function 
		check_status = True
		proxy = "{}:{}".format(ip, port)
		print("[*] Checking: {}".format(proxy))
		try:
			proxy_sock5 = {
				'http' : "socks5://{}".format(proxy),
	    		'https' : "socks5://{}".format(proxy),
			}
			self.send_req(proxy_sock5, proxy, "SOCK5")
			check_status = False
		except Exception as e:
			pass
		if(check_status == True):
			try:
				proxy_sock4 = {
					'http' : "socks4://{}".format(proxy),
		    		'https' : "socks4://{}".format(proxy),
				}
				self.send_req(proxy_sock4, proxy, "SOCK4")
				check_status = False
			except Exception as e:
				pass	
		if(check_status == True):
			try:
				proxy_http = {
					'http' : "http://{}".format(proxy),
		    		'https' : "https://{}".format(proxy),
				}
				self.send_req(proxy_http, proxy, "HTTP")	
			except Exception as e:
				pass
	def send_req(self, proxydict, proxy, proxy_type): 
		#This block send q request to self.url variable then save the proxy
		#depends on it's type
		req = requests.get(self.url, proxies=proxydict, timeout=5)
		if(req.status_code == 200):
			if(proxy_type == "SOCK5"):
				file = open('sock5.txt', 'a')
				file.write(proxy+"\n")
				file.close()
			elif(proxy_type == "SOCK4"):
				file = open('sock4.txt', 'a')
				file.write(proxy+"\n")
				file.close()
			elif(proxy_type == "HTTP"):
				file = open('http.txt', 'a')
				file.write(proxy+"\n")
				file.close()
			else:
				print("{} - proxy type not found".format(proxy))
			self.goodProxy += 1
			print("[*] You successfully send request using the proxy: {}".format(req.text.strip('\n')))
			print("[*] {} is a {} proxy".format(proxy, proxy_type))
		else:
			print("[*] Failed to send request using {} proxy".format(proxy))

proxyChecker = ProxyChecker()
try:
	proxyChecker.main()
except KeyboardInterrupt:
	print("Proxy Checker is now offline.")
	sys.exit(1)