#!/usr/bin/env python3
##########################################
# Duino-Coin Multitool (v1.5) 
# https://github.com/revoxhere/duino-coin 
# Distributed under MIT license
# © revox and phantom32 2020
##########################################

import socket, hashlib, os, urllib.request # Only python3 included libraries
soc = socket.socket()

client_version = "1.5"

serverip = "https://raw.githubusercontent.com/revoxhere/duino-coin/gh-pages/serverip.txt" # Serverip file

print("\nDuino-Coin Multitool v1.5")
print("Made by revox and phantom32" +"\n")

print("Please enter your credentials to continue")
username = input("Username: ")
password = input("Password: ")

try:
    with urllib.request.urlopen(serverip) as content:
        content = content.read().decode().splitlines() #Read content and split into lines
        pool_address = content[0] #Line 1 = pool address
        pool_port = content[1] #Line 2 = pool port
        print("\nServer address: " + pool_address + ":" + pool_port + "\n")
except:
    print("Can't get server address, check your internet connection.")
    print("Thanks for using Duinocoin Multitool!")
    os._exit(0)

print("Connecting to the server...\n")

# This section connects and logs user to the server
try:
    soc.connect((str(pool_address), int(pool_port))) # Connect to the server
    server_version = soc.recv(3).decode() # Get server version
    print("Connection established, server is on version " + server_version + "\n")

    if server_version != client_version:
        print("Server upgraded to a new version")
        print("This client may not work with the server")
        print("Do you still want to continue?")
        if input("Yes (y), No(n) >") == "y" and "Y":
            pass
        else:
            print("Thanks for using Duinocoin Multitool!")
            os._exit(0)
except:
    print("Can't connect to the server.\nIt is probably under maintenance or temporarily down.\n")
    print("Thanks for using Duinocoin Multitool!")
    os._exit(0)

print("Logging in with username and password...")


soc.send(bytes("LOGI," + str(username) + "," + str(password), encoding="utf8"))
loginFeedback = soc.recv(128).decode().split(",")
if loginFeedback[0] == "OK":
    print("Successfully logged in with username: " + username)
    pass
else:
	print("Couldn't login, reason: " + str(loginFeedback[1]))

	os._exit(0)

print("Type `help` to list available commands")
print("Press enter to refresh the balance\n")

while True:
    soc.send(bytes("BALA", encoding="utf8"))
    balance = round(float(soc.recv(256).decode()), 8)
    print("Balance: ")
    print(balance)
    command = input("> ")

    if command == "help":
        print("help: displays available commands")
        print("send: sends funds")
        print("userinfo: displays user info")
        print("changepass: changes user password")
        print("exit: exits duino multitool")
        print("about: displays wallet information\n")
    
    elif command == "send":
        recipient = input("Enter recipients' username: ")
        amount = input("Enter amount to transfer: ")
        soc.send(bytes("SEND,deprecated,"+str(recipient)+","+str(amount), encoding="utf8"))
        while True:
            message = soc.recv(1024).decode()
            print("Server message: " + str(message))
            break
    
    elif command == "userinfo":
        soc.send(bytes("STAT", encoding="utf8"))
        while True:
            message = soc.recv(1024).decode()
            break
        print("Server message: " + str(message))
    
    elif command == "changepass":
        oldpassword = input("Enter your current password: ")
        newpassword = input("Enter new password: ")
        soc.send(bytes("CHGP,"+  str(oldpassword) + "," + str(newpassword), encoding="utf8"))
        while True:
            message = soc.recv(1024).decode()
            print("Server message: " + str(message))
            break
    
    elif command == "exit":
        print("Closing connection...")
        try:
            soc.send(bytes("CLOSE", encoding="utf8"))
            print("Closed connection to the server\n")
        except:
            pass
        print("Thanks for using Duinocoin Multitool!")
        os._exit(0)

    elif command == "about":
        print("Duinocoin Multitool")
        print("Made by revox and phantom32 2020")
        print("Client version: " + client_version)
        print("https://github.com/revoxhere/duino-coin")

    else:
        continue
