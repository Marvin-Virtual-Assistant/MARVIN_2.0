#Imports
from webbrowser import open as webopen # webbrowser to open websites
import marvin.essentials # import speak and listen
import marvin.webscrape # import webscrape functions
from json import load, dump # import json load
from threading import Thread
import os
import marvin.misc
import time
from datetime import datetime
import marvin.send_email


#####################
# File for commands #
#####################


#COMMANDS

class MarvinCommands(Exception): pass
class MarvinRelog(Exception): pass
def dataCommands(command, type_of_input, pass_path, contact_path):


    # Website Commands #

    if 'open reddit' in command:
        subreddit = command.split(" ")[2:] # split for anything after 'open reddit'
        subreddit_joined = (" ").join(subreddit) # joining anything that was split from after 'open reddit'
        essentials.speak('Opening subreddit ' + subreddit_joined) # saying the subreddit page
        url = ('https://www.reddit.com/r/' + subreddit_joined) # url with reddit page
        webopen(url, new = 2) # open url in browser
        print('Done!')

    elif 'rotten tomatoes' in command:
        rotten_search = command.split(" ")[2:] # split for anything after 'rotten tomatoes'
        rotten_joined = (" ").join(rotten_search)
        webscrape.scrapeRottentomatoes(rotten_joined)

    elif 'imdb' in command:
        IMDb_search = command.split(" ")[1:] # split for anything after 'rotten tomatoes'
        IMDb_joined = (" ").join(IMDb_search)
        webscrape.IMDb(IMDb_joined)

    elif 'imdb rating' in command:
        IMDb_search = command.split(" ")[2:] # split for anything after 'imdb rating'
        IMDb_joined = (" ").join(IMDb_search)
        webscrape.IMDb(IMDb_joined)

    elif 'google search' in command:
        gsearch = command.split(" ")[2:] # split for anything after 'google search'
        gsearch_joined = (" ").join(gsearch) # joining anything that was split from after 'google search'
        essentials.speak('Opening Google search for ' + gsearch_joined) # saying what it will open
        url = ('https://www.google.com/search?q=' + gsearch_joined + '&rlz=1C5CHFA_enUS770US770&oq=' + gsearch_joined + '&aqs=chrome..69i57.1173j0j8&sourceid=chrome&ie=UTF-8') # url with search
        webopen(url, new = 2) # open url in browser
        print('Done!')

    elif 'youtube' in command:
        video = command.split(" ")[1:] # split for anything after 'youtube'
        video_joined = (" ").join(video) # joining anything that was split from after 'youtube'
        essentials.speak('Opening first video for ' + video_joined + ' on YouTube') # saying what it will open
        webscrape.scrapeYoutube(video_joined) # function to scrape urls

    elif 'where is' in command:
        location = command.split(" ")[2:] # split for anything after 'where is'
        location_joined = (" ").join(location) # joining anything that was split from after 'where is'
        essentials.speak('Hold on, I will show you where ' + location_joined + ' is.') # saying the location heard
        url = ('https://www.google.nl/maps/place/' + location_joined + '/&amp;') # url with location
        webopen(url, new = 2) # open url in browser
        print('Done!')

    elif 'amazon' in command:
        amazon = command.split(" ")[1:] # split for anything after 'amazon'
        amazon_search = (" ").join(amazon) # join all anything after 
        essentials.speak('Searching amazon for ' + amazon_search) # saying what it will look for
        url = ('https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + amazon_search) # url with amazon search
        webopen(url, new = 2) # open in browser
        print('Done!')

    elif 'time in' in command:
        time_in = command.split(" ")[2:] # split for anything after 'time in'
        time_in_location = (" ").join(time_in) # joiing anything after 'time in'
        essentials.speak('Showing time in '+ time_in_location) # saying what its opening
        url = ('https://time.is/' + time_in_location) # url to time.is with the location
        webopen(url, new = 2) # open in browser
        print('Done!')

    # Marvin Function Commands #

    elif 'standby' in command:
        essentials.speak('Going on standby')
        raise MarvinCommands # raise exeption so class passes and restarts loop

    elif command == 'exit' or command == 'quit' or command == 'leave' or command == 'close':
        essentials.speak('Shutting down')
        exit() # leave program

    elif command == 'relog' or command == 'logout' or command == 'log out':
        essentials.speak('logging out')
        raise MarvinRelog

    elif command == 'ls' or command == 'dir':
        with open('.Os.json', 'r') as os_data:
            os_system_data = load(os_data)
        os_system = os_system_data['Os_data']['OS']
        if os_system == 'Linux':
            os.system('ls')
        elif os_system == 'Darwin':
            os.system('ls')
        elif os_system == 'Windows':
            os.system('dir')

    # Sending based Commands

    elif command == 'contact list' or command == 'contacts':
        contacts.contactList(contact_path, 0)

    elif command == 'delete contact' or command == 'remove contact':
        try:
            contacts.contactList(contact_path, 1)
            print('input cancel to cancel delete contact') # cancel message
            essentials.speak('Who would you like to delete from your contacts?')
            delete_contact = essentials.commandInput(type_of_input).lower() # function for listen or raw_input
            if 'quit' == delete_contact.lower() or 'exit' == delete_contact.lower() or 'cancel' == delete_contact.lower(): raise ValueError # check message for cancel
            with open(contact_path, 'r') as contact_del_list:
                del_contact_data = load(contact_del_list)
            if delete_contact.lower() not in del_contact_data['contacts']: 
                print('User does not exist')
                raise ValueError
            del del_contact_data['contacts'][delete_contact]
            with open(contact_path, 'w') as outfile:
                dump(del_contact_data, outfile)
        except Exception as e:
            print('cancelling')

    elif command == 'add contact' or command == 'new contact':
        try:
            contacts.contactList(contact_path, 1)
            print('input cancel to cancel add contact') # cancel message
            essentials.speak('Who would you like to add to you contacts?')
            print('First name please')
            add_contact = essentials.commandInput(type_of_input) # function for listen or raw_input
            if 'quit' == add_contact.lower() or 'exit' == add_contact.lower() or'cancel' == add_contact.lower(): raise ValueError # check message for cancel
            print('input cancel to cancel add contact') # cancel message
            essentials.speak('What is ' + add_contact + '\'s email?')
            new_email = essentials.commandInput(type_of_input) # function for listen or raw_input
            if 'quit' == new_email.lower() or 'exit' == new_email.lower() or 'cancel' == new_email.lower(): raise ValueError # check message for cancel
            print('input cancel to cancel add contact') # cancel message
            essentials.speak('What is ' + add_contact + '\'s phone number? If you don\'t have it or you dont want to input respond with None')
            new_phone_number = essentials.commandInput(type_of_input) # function for listen or raw_input
            if 'quit' == new_phone_number.lower() or 'exit' == new_phone_number.lower() or 'cancel' == new_phone_number.lower(): raise ValueError # check message for cancel
            essentials.speak('Does this contact have a nickname you like to add? If they don\'t have one type none')
            nick = essentials.commandInput(type_of_input) # function for listen or raw_input
            nick_lower = nick.lower()
            if 'quit' == nick_lower or 'exit' == nick_lower or 'cancel' == nick_lower: raise ValueError # check message for cancel
            with open(contact_path, 'r') as contact_data:
                new_contact_data = load(contact_data) # read data
            if 'none' != nick_lower:
                new_contact_data['nicks'][nick_lower] = {"real_name":add_contact_lowered}
            essentials.speak('Creating contact')
            add_contact_lowered = add_contact.lower()
            with open(contact_path, 'w') as outfile:
                new_contact_data['contacts'][add_contact_lowered] = {"email":new_email, "number":new_phone_number} # new data to add
                dump(new_contact_data, outfile) # add data
            print('Contact Created!')
        except Exception as e:
            print('cancelling')

    elif command == 'send email':
        try:
            contacts.contactList(contact_path, 'email')
            print('input cancel to cancel send email') # cancel message
            essentials.speak('Who would you like to send this email to?')
            email_recipient = essentials.commandInput(type_of_input) # function for listen or raw_input
            if 'quit' == email_recipient.lower() or 'exit' == email_recipient.lower() or 'cancel' == email_recipient.lower(): raise ValueError # check message for cancel
            print('input cancel to cancel send email') # cancel message
            essentials.speak('What is the subject of the email?')
            email_subject = essentials.commandInput(type_of_input) # function for listen or raw_input
            if 'quit' == email_subject.lower() or 'exit' == email_subject.lower() or 'cancel' == email_subject.lower(): raise ValueError # check message for cancel
            print('input cancel to cancel send email') # cancel message
            essentials.speak('What is the message you would like to send to ' + email_recipient)
            email_body = essentials.commandInput(type_of_input) # function for listen or raw_input
            if 'quit' == email_body.lower() or 'exit' == email_body.lower() or 'cancel' == email_body.lower(): raise ValueError # check message for cancel
            thread_email = Thread(target = send_email.email, args = (email_recipient, email_subject, email_body, pass_path, contact_path,))
            thread_email.start()
        except Exception as e:
            print('cancelling')

    # Misc Commands #
    elif command == 'what time is it':
        essentials.speak('The time is ' + datetime.now().strftime('%-I:%M %p'))

    elif command == 'what is the date':
        essentials.speak('The date is ' + datetime.now().strftime('%A %B %-d %Y'))

    elif command == "day of the week":
        essentials.speak(datetime.now().strftime('%A'))

    elif command == "week number":
        essentials.speak(datetime.now().strftime('%W'))

    elif command == 'open calculator' or command == 'run calculator' or command == 'calculator':
        thread_calculator = Thread(target = misc.openCalculator) # run calculator code from calculator.py
        print('Calculator Opened!') # open message
        thread_calculator.start() # start 2nd thread with calulator so you can run commands along with the calculator open

    elif command == 'open stopwatch' or command == 'run stopwatch' or command == 'stopwatch':
        thread_stopwatch = Thread(target = misc.openStopwatch) # run calculator code from calculator.py
        print('Stopwatch Opened!') # open message
        thread_stopwatch.start() # start 2nd thread with calulator so you can run commands along with the calculator open

    elif command == 'hello' or command == 'hi':
        essentials.speak('Hello!')