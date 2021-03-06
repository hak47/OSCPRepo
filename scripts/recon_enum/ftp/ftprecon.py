#!/usr/bin/env python
import subprocess
import sys
import os

if len(sys.argv) != 3:
    print "Usage: ftprecon.py <ip address> <port>"
    sys.exit(0)

ip_address = sys.argv[1].strip()
port = sys.argv[2].strip()

#NSE Script documentation
#RUNNING
#ftp-anon: checks if FTP server allows anonymous logins, if so, get a dir listing
#ftp-bounce: checks if FTP server allows port scanning using the FTP bounce method, see https://en.wikipedia.org/wiki/FTP_bounce_attack
#ftp-proftpd-backdoor: check for ProFTPD 1.3.3c backdoor, OSVDB-ID 69562. If vuln, telnet or ftp and send: "HELP ACIDBITCHEZ"
#ftp-syst: sends SYST and STAT commands and returns result. SYST asks for OS info. STAT asks for server status. see https://cr.yp.to/ftp/syst.html
#ftp-vsftpd-backdoor: check for vsFTPd 2.3.4 backdoor CVE-2011-2523, send a :) and potential to execute a command
#ftp-vuln-cve-2010-4221: check for stack-based buffer overflow in ProFTPD server between 1.3.2rc3 and 1.3.3b. May crash the ftp service. Default tries to run nmap. Check exploit-db. 
#tftp-enum: brute's a default list of file names to determine if they are available on the server. have to manually tftp {IP} get {filename} if discovered.
#TFTP is UDP protocol make sure it's handled correctly

#NOT RUNNING
#ftp-brute: perform brute force against FTP
#ftp-libopie: check for CVE-2010-1938, WARNING will crash if vulnerable, better to manually check...

print "INFO: Performing nmap FTP script scan for " + ip_address + ":" + port
FTPSCAN = "nmap -n -sV -Pn -vv -p %s --script=ftp-anon,ftp-bounce,ftp-syst,ftp-proftpd-backdoor,ftp-vsftpd-backdoor,ftp-vuln-cve2010-4221,tftp-enum,vulners -oN '/root/scripts/recon_enum/results/exam/ftp/%s_ftp.nmap' %s" % (port, ip_address, ip_address)
results = subprocess.check_output(FTPSCAN, shell=True)
outfile = "/root/scripts/recon_enum/results/exam/ftp/" + ip_address + "_ftprecon.txt"
f = open(outfile, "w")
f.write(results)
f.close

#Default Hydra configuration with a small username and password list
#This configuration is meant to spray, not to brute. Manually configure a 
#Brute scan if desired.

print "INFO: Performing hydra ftp scan against " + ip_address 
HYDRAFTP = "hydra -L /usr/share/wordlists/lists/userlist.txt -P /usr/share/wordlists/lists/quick_password_spray.txt -f -o /root/scripts/recon_enum/results/exam/ftp/%s_ftphydra.txt -u %s -s %s ftp" % (ip_address, ip_address, port)
try:
    results = subprocess.check_output(HYDRAFTP, shell=True)
    resultarr = results.split("\n")
    for result in resultarr:
        if "login:" in result:
	        print "[*] Valid ftp credentials found: " + result
except:
    print "INFO: No valid ftp credentials found"
