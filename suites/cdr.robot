*** Settings ***
Library    /home/ats/ATS/kqa/library/cdr/CDRouterLibrary.py
Library    /home/ats/ATS/kqa/library/terminal/DeviceTerminal.py
Library    /home/ats/ATS/kqa/library/utils/TableVerificationLibrary.py

*** Variables ***
${PACKAGE_NAME}    QA/General/IPv4(DHCP)
${VERIFY_INFO}     SEPARATOR=${EMPTY}
...
...    | Name                     | Configuration        | Device                    | \n
...    | QA/General/IPv4(DHCP)    | QA-General_PG2142    | QA_PG2142/KAONCE1A9C3E    | \n

*** Test Cases ***
Run CDR Test
    [Setup]                        Test Setup
    Test Connection
    Launch Job And Check Status

*** Keywords ***
Establish Connection
    [Arguments]            ${device_name}
    ${cdrouter_info}       Get Device Info    ${device_name}
    Set Test Variable      ${CDR_PATH}        ${cdrouter_info['connections']['path']}
    Set Test Variable      ${CDR_USERNAME}    ${cdrouter_info['custom']['username']}
    Set Test Variable      ${CDR_PASSWORD}    ${cdrouter_info['custom']['password']}
    Connect To Cdrouter    ${CDR_PATH}        ${CDR_USERNAME}                            ${CDR_PASSWORD}

Test Connection
    Establish Connection    CDRouter
    ${package}              Get Package By Name         ${PACKAGE_NAME}
    ${package_info}         Get Package Info By Name    ${PACKAGE_NAME}

    ${package_info}    Create Table    ${package_info}
    ${veriry_table}    Create Table    ${VERIFY_INFO}

    ${result}         Verify Table    ${veriry_table}    ${package_info}    whitelist
    Should Be True    ${result}

Launch Job And Check Status
    ${package_id}                Get Package Id By Name    ${PACKAGE_NAME}
    ${job_id}                    Set Launch Job            ${package_id}
    Check Until Job Completed    ${job_id}

Check Result From CDR
    ${result_id}    Get Result Id From Job    ${job_id}
    ${result}       Get Result By Id          ${result_id}

Test Setup
    Load Topology    /home/ats/ATS/kqa/suites_data/topology.yaml