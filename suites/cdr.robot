*** Settings ***
Library    /home/ats/ATS/kqa/library/cdr/CDRouterLibrary.py

*** Variables ***

*** Test Cases ***
Test Connection
    Connect To Cdrouter    http://192.168.150.240    KVINQA    kaon1234
    ${list_pkg}   Get All Id Packages
    Log To Console    ${list_pkg}
*** Keywords ***
