*** Settings ***
Documentation    This is a resource file, that can contain variables and keywords.
...              Keywords defined here can be used where this Keywords.resource in loaded.
Library          /home/ats/ATS/kqa/library/DeviceTerminal.py
Library          Telnet

*** Keywords ***

### Setup Connection ###
Connect To Switch
    ${device_info}       Get Device Info    ${DEVICE_NAME}
    Set Test Variable    ${HOST1}           ${device_info['connections']['ip']}
    Set Test Variable    ${PORT1}           ${device_info['connections']['port']}
    Set Test Variable    ${USERNAME1}       ${device_info['connections']['username']}
    Set Test Variable    ${PASSWORD1}       ${device_info['connections']['password']}
    Open Connection      ${HOST1}
    Login                ${USERNAME1}       ${PASSWORD1}
    Write                enable

Connect To Olt
    Connect To Switch
    ${device_info2}      Get Device Info    ${DEVICE_OLT}
    Set Test Variable    ${HOST2}           ${device_info2['connections']['ip']}
    Set Test Variable    ${PORT2}           ${device_info2['connections']['port']}
    Set Test Variable    ${USERNAME2}       ${device_info2['connections']['username']}
    Set Test Variable    ${PASSWORD2}       ${device_info2['connections']['password']}
    Open Connection      ${HOST2}
    Login                ${USERNAME2}       ${PASSWORD2}
    Write                enable

### Send Command ###

Send Command To Config Mode
    [Arguments]        ${command}
    Update Prompt
    Write              configure terminal
    Update Prompt
    Execute Command    ${command}

Update Prompt
    ${prompt}     Read Until Regexp    (#|>)
    Log           ${prompt.strip()}
    Set Prompt    ${prompt.strip()}

