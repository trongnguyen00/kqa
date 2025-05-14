*** Settings ***
Library    /home/ats/ATS/kqa/library/cdr/CDRouterLibrary.py
Library    /home/ats/ATS/kqa/library/terminal/TopologyLoader.py
Library    /home/ats/ATS/kqa/library/utils/TableVerificationLibrary.py
Library    OperatingSystem
Library    Telnet
Library    Process

*** Variables ***
${PACKAGE_NAME_V4}        QA/General/IPv4(DHCP)
${PACKAGE_NAME_DSLITE}    QA/PG6692G/DS-LITE
${PACKAGE_NAME_DEMO}      QA/General/IPv4(DHCP)_TRONG

${VERIFY_INFO_DSLITE}    SEPARATOR=${EMPTY}
...
...    | Name                  | Configuration         | \n
...    | QA/PG6692G/DS-LITE    | QA-PG6692G-DS-LITE    | \n


${VERIFY_INFO_V4}    SEPARATOR=${EMPTY}
...
...    | Name                     | Configuration                     | \n
...    | QA/General/IPv4(DHCP)    | [QA]PG6692G-General-IPv4(DHCP)    | \n


${VERIFY_INFO_DEMO}    SEPARATOR=${EMPTY}
...
...    | Name                           | Configuration                     | \n
...    | QA/General/IPv4(DHCP)_TRONG    | [QA]PG6692G-General-IPv4(DHCP)    | \n


*** Test Cases ***
Test Dhcp4 Package
    [Documentation]    Test case: change WAN ONT configuration and Run CDRouter packet with notify via email
    [Setup]            Test Setup

    Change Wan Ont To Dhcp4
    CDRouter Run Test Dhcp4

Test Dslite Package
    [Documentation]    Test case: change WAN ONT configuration and Run CDRouter packet with notify via email
    [Setup]            Test Setup

    Change Wan Ont To Dslite
    CDRouter Run Test Dslite

*** Keywords ***
CDRouter Run Test Dhcp4
    [Documentation]    Run CD Router with package QA/General/IPv4(DHCP)_TRONG

    Test Connection And Verify Package    ${PACKAGE_NAME_DEMO}    ${VERIFY_INFO_DEMO}
    Launch Job And Check Status           ${PACKAGE_NAME_DEMO}
    Check Result From CDR
    Run Process                           python3                 send_robot.py          cwd=/home/ats/ATS/kqa

CDRouter Run Test Dslite
    [Documentation]    Run CD Router with package QA/PG6692G/DS-LITE

    Test Connection And Verify Package    ${PACKAGE_NAME_DSLITE}    ${VERIFY_INFO_DSLITE}
    Launch Job And Check Status           ${PACKAGE_NAME_DSLITE}
    Check Result From CDR
    Run Process                           python3                   send_robot.py            cwd=/home/ats/ATS/kqa

Change Wan Ont To Dhcp4
    [Documentation]    Step to change WAN configuration of ONT to DHCPv4 and check configuration.

    [Teardown]                     Close All Connections
    Connect To Ont                 Onu0
    Wait Until Keyword Succeeds    5x                       5s    Set Wan To Dhcp4
    Reboot Ont
    Wait Until Keyword Succeeds    5x                       5s    Check Wan Dhcp4 Is Configured

Change Wan Ont To Dslite
    [Documentation]    Step to change WAN configuration of ONT to DsLite and check configuration.

    [Teardown]                     Close All Connections
    Connect To Ont                 Onu0
    Wait Until Keyword Succeeds    5x                       5s    Set Wan To Dslite
    Reboot Ont
    Wait Until Keyword Succeeds    5x                       5s    Check Wan Dslite Is Configured

Reboot Ont
    [Documentation]    Perform reboot ONT and wait 120s
    Execute Command    reboot
    Sleep              120s
    Write Bare         \r\n

Establish Connection
    [Documentation]    Create connection with CDRouter

    [Arguments]            ${device_name}
    ${cdrouter_info}       Get Device Info    ${device_name}
    Set Test Variable      ${CDR_PATH}        ${cdrouter_info['connections']['path']}
    Set Test Variable      ${CDR_USERNAME}    ${cdrouter_info['custom']['username']}
    Set Test Variable      ${CDR_PASSWORD}    ${cdrouter_info['custom']['password']}
    Connect To Cdrouter    ${CDR_PATH}        ${CDR_USERNAME}                            ${CDR_PASSWORD}

Test Connection And Verify Package
    [Documentation]    Connect to CDrouter and checking valid package's information

    [Arguments]             ${packet_name}              ${verify_info}
    Establish Connection    CDRouter
    ${package}              Get Package By Name         ${packet_name}
    ${package_info}         Get Package Info By Name    ${packet_name}

    ${package_info}    Create Table    ${package_info}
    ${veriry_table}    Create Table    ${verify_info}

    ${result}         Verify Table    ${veriry_table}    ${package_info}    whitelist
    Should Be True    ${result}

Launch Job And Check Status
    [Documentation]    Start run a package on CDRouter and trigger running

    [Arguments]                  ${packet_name}
    ${package_id}                Get Package Id By Name    ${packet_name}
    ${job_id}                    Set Launch Job            ${package_id}
    Check Until Job Completed    ${job_id}
    ${result_id}                 Get Result Id From Job    ${job_id}
    Set Test Variable            ${result_id}

Check Result From CDR
    [Documentation]    Get result from CDRouter and export result to prepare email

    ${result}                Get Result By Id    ${result_id}
    ${msg}                   ${status}           Get Result Msg    ${result_id}
    Export Result To Csv     ${result_id}
    Check Is Error Result    ${result_id}

Connect To Ont
    [Documentation]    Connect To ONT console via Moxa interface

    [Arguments]          ${device_name}
    ${device_info}       Get Device Info    ${device_name}
    Set Test Variable    ${HOST}            ${device_info['connections']['ip']}
    Set Test Variable    ${PORT}            ${device_info['connections']['port']}}
    Open Connection      host=${HOST}       port=4008                                 prompt=root@prplOS:~# 

Check Wan Dhcp4 Is Configured
    [Documentation]    Checking WAN DHCP4 is configured successfully

    ${wan_status}     Execute Command    ba-cli WANManager.WAN.vlanmode.Intf.wan.IPv4Mode?
    Should Contain    ${wan_status}      dhcp4

Check Wan Dslite Is Configured
    [Documentation]    Checking WAN DSlite is configured successfully

    ${wan_status}     Execute Command    ba-cli WANManager.WAN.vlanmode.Intf.wan.IPv4Mode? 
    Should Contain    ${wan_status}      dslite

Set Wan To Dhcp4
    [Documentation]    Set configure DHCP4 for WAN ONT and check config successful or not

    Execute Command                  ba-cli WANManager.WAN.vlanmode.Intf.wan.IPv4Mode=dhcp4
    Execute Command                  ba-cli WANManager.WAN.vlanmode.Intf.wan.IPv4Reference=Device.IP.Interface.2.
    Check Wan Dhcp4 Is Configured

Set Wan To Dslite
    [Documentation]    Set configure Dslite for WAN ONT and check config successful or not

    Execute Command                   ba-cli WANManager.WAN.vlanmode.Intf.wan.IPv4Mode=dslite
    Execute Command                   ba-cli WANManager.WAN.vlanmode.Intf.wan.IPv4Reference=Device.IP.Interface.7.
    Check Wan Dslite Is Configured

Test Setup
    [Documentation]    Load topology file
    Load Topology      /home/ats/ATS/kqa/suites_data/topology.yaml