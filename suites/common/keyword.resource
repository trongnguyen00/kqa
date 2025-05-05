*** Settings ***
Documentation    This is a resource file, that can contain variables and keywords.
...              Keywords defined here can be used where this Keywords.resource in loaded.
Library          /home/ats/ATS/kqa/library/DeviceTerminal.py
Library          /home/ats/ATS/kqa/library/TerminalCommands.py
Library          /home/ats/ATS/kqa/library/TableVerificationLibrary.py
Library          /home/ats/ATS/kqa/library/pixia/library.py
Library          Telnet

*** Keywords ***

### Setup Connection ###
Connect To Dut
    [Arguments]          ${device_name}
    ${device_info}       Get Device Info    ${device_name}
    Set Test Variable    ${HOST1}           ${device_info['connections']['ip']}
    Set Test Variable    ${PORT1}           ${device_info['connections']['port']}
    Set Test Variable    ${USERNAME1}       ${device_info['connections']['username']}
    Set Test Variable    ${PASSWORD1}       ${device_info['connections']['password']}
    Open Connection      ${HOST1}
    Login                ${USERNAME1}       ${PASSWORD1}
    Set Prompt           .*>                prompt_is_regexp=${True}
    Sleep                3

Open Connection With Current Connection
    [Arguments]          ${device_name}
    ${device_info}       Get Device Info    ${device_name}
    Set Test Variable    ${HOST1}           ${device_info['connections']['ip']}
    Set Test Variable    ${PORT1}           ${device_info['connections']['port']}
    Set Test Variable    ${USERNAME1}       ${device_info['connections']['username']}
    Set Test Variable    ${PASSWORD1}       ${device_info['connections']['password']}
    Write                telnet ${HOST1}
    Login                ${USERNAME1}       ${PASSWORD1}
    Set Prompt           .*>                prompt_is_regexp=${True}
    Sleep                3

Get Ixia Connection
    ${ixia_info}         Get Device Info    IXIA
    Set Test Variable    ${ixia_ip}         ${ixia_info['connections']['ip']}
    Set Test Variable    ${ixia_session}    ${ixia_info['custom']['session_id']}
    RETURN               ${ixia_ip}         ${ixia_session}

### Send Command ###
Set Terminal Length
    [Arguments]              ${length}=0
    Send Command Terminal    terminal length ${length}

Send Command Terminal
    [Arguments]    ${command}
    ${loginfo}     Execute Command    ${command}
    RETURN         ${loginfo}

Auto Detect And Set Prompt
    [Documentation]    Tự động đọc prompt từ đầu ra và set prompt cho phiên kết nối hiện tại

    ${output}=       Read Until Regexp    [>#$]
    ${last_line}=    Evaluate             '''${output}'''.splitlines()[-1]    modules=builtins
    Set Prompt       ${last_line}