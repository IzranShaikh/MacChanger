#!/usr/bin/env python


#MODULES
import subprocess as sp
import scapy.all as scapy
import optparse
import time
import re


#TITLE
sp.call("clear;figlet -f standard 'MAC CHANGER'",shell=True)


#WHILE !EXCEPTIONS
try:


	#GLOBAL VARIABLES
	BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END, BOLD, UNDERLINE, PURPLE, CYAN, DARKCYAN = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m', '\033[1m', '\033[4m', '\033[95m', '\033[96m', '\033[36m'


	#CLASS-METHODS
	class MACCHANGER:
		def get_mac_of_interface(self):
			self.interface = raw_input("Enter the Interface Name(you want to see MAC of)\n>>")
			self.ifconfig_result = sp.check_output(["ifconfig",self.interface])
			self.pattern_for_extracting_mac = "(?:\s)(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)(?:\s)"
			self.mac = re.search(self.pattern_for_extracting_mac,self.ifconfig_result).group(1)
			print(GREEN+"\nYour Current MAC Address of "+str(self.interface)+" : "+str(self.mac)+END)

		def backup_mac(self):
			self.interface = raw_input("Enter the Interface Name(you want to store MAC of)\n>>")
			self.ifconfig_result = sp.check_output(["ifconfig",self.interface])
			print(YELLOW+"\n[+] Getting your MAC Address ...\n"+END)
			self.mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",self.ifconfig_result)
			time.sleep(1)
			if not self.mac_address_search_result:
				print(RED+"[!] Could not find your MAC Address!"+END)
				main()
			self.original_mac_address = self.mac_address_search_result.group(0)#group(0) 0=occurance
			print(GREEN+"Your Current MAC Address: "+self.original_mac_address+END)
			if self.interface=="eth0":
				self.original_mac_address_file = open("original_mac_address.txt","w")
				print(YELLOW+"\n[+] Backing Up Your MAC Address\n"+END)
				self.original_mac_address_file.write(self.original_mac_address)
				time.sleep(1)
				self.original_mac_address_file.close()
				print(GREEN+"[+] MAC Address Successfully Backed Up!"+END)
			elif self.interface=="wlan0":
				self.wlan_mac_address_file = open("wlan_mac_address.txt","w")
				print(YELLOW+"\n[+] Backing Up Your MAC Address\n"+END)
				self.wlan_mac_address_file.write(self.original_mac_address)
				time.sleep(1)
				self.wlan_mac_address_file.close()
				print(GREEN+"[+] MAC Address Successfully Backed Up!"+END)
			else:
				print(RED+"[!] NO SUCH INTERFACE or DEVICE"+END)

		def change_mac(self):
			self.interface = str(raw_input("Enter interface(to change MAC of)\n>>"))
			self.new_mac = raw_input("Enter New MAC\n>>")
			time.sleep(1)
			sp.call(["ifconfig", self.interface, "down"])
			print("\n"+BLUE+"[+]"+" Changing MAC of "+END+self.interface+BLUE+" to "+END+self.new_mac+"\n")
			sp.call(["ifconfig", self.interface, "hw", "ether", self.new_mac])
			sp.call(["ifconfig", self.interface, "up"])
			time.sleep(2)
			print(GREEN+"[+] MAC Address Successfully Changed!"+END)

		def restore_mac(self):
			self.interface = raw_input("Enter the Interface Name(you want to restore MAC of)\n>>")
			if self.interface=="eth0":
				self.original_mac_address_file = open("original_mac_address.txt","r")
				self.mac_address_to_restore = self.original_mac_address_file.read()
				if self.mac_address_to_restore=='':
					print(RED+"\n[-] You didn't Backed Up Your MAC Address"+END)
				else:
					print(BLUE+"\nYour Stored MAC Address : "+END+self.mac_address_to_restore)
					print(YELLOW+"\n[+] Restoring Your Stored MAC Address Back ...\n"+END)
					sp.call(["ifconfig", self.interface, "down"])
					sp.call(["ifconfig", self.interface, "hw", "ether", self.mac_address_to_restore])
					sp.call(["ifconfig", self.interface, "up"])
					time.sleep(2)
					print(GREEN+"[+] MAC Address("+self.mac_address_to_restore+") Successfully Restored."+END)
			elif self.interface=="wlan0":
				self.wlan_mac_address_file = open("wlan_mac_address.txt","r")
				self.mac_address_to_restore = self.wlan_mac_address_file.read()
				if self.mac_address_to_restore=='':
					print(RED+"\n[-] You didn't Backed Up Your MAC Address"+END)
				else:
					print(BLUE+"\nYour Stored MAC Address : "+END+self.mac_address_to_restore)
					print(YELLOW+"\n[+] Restoring Your Stored MAC Address Back ...\n"+END)
					sp.call(["ifconfig", self.interface, "down"])
					sp.call(["ifconfig", self.interface, "hw", "ether", self.mac_address_to_restore])
					sp.call(["ifconfig", self.interface, "up"])
					time.sleep(2)
					print(GREEN+"[+] MAC Address("+self.mac_address_to_restore+") Successfully Restored."+END)
			else:
				print(RED+"\n[!] NO SUCH INTERFACE or DEVICE CONNECTED"+END)

		def main(self):
			self.choice = int(raw_input('\n{0}[{1}1{0}]{1} Show My MAC  {0}[{1}2{0}]{1} Change MAC  {0}[{1}3{0}]{1} Backup MAC  {0}[{1}4{0}]{1} Restore MAC  {0}[{1}5{0}]{1} Quit  '.format(YELLOW, WHITE) + '\n>>'))
			if self.choice==1:
				self.get_mac_of_interface()
			elif self.choice==2:
				self.change_mac()
			elif self.choice==3:
				self.backup_mac()
			elif  self.choice==4:
				self.restore_mac()
			elif self.choice==5:
					print(RED+"\n[-] EXITING...")
					time.sleep(1)
					print(GREEN+"\nThanks For Using MAC CHANGER...\n"+END)
					quit()
			else:
				print(RED+"\n[-] INVALID OPTION"+END)


	#MAIN
	Mc = MACCHANGER()
	while True:
		Mc.main()


#EXCEPTION HANDLING
except KeyboardInterrupt:
	print(RED+"\n\n[!] KeyboardInterrupt Occured!!!\nExiting ...\n"+END)
	quit()
