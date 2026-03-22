import pywhatkit

# Enter phone number (with country code: +90...)
number = input("Enter phone number (+90...): ")


# Enter message
message = input("Enter message: ")

# Send message
# wait_time: Wait 15 seconds for the page to load.
# tab_close: Close the tab after the message is sent.
pywhatkit.sendwhatmsg_instantly(number, message, wait_time=25, tab_close=True)
