*** Settings ***
Library    /home/ats/ATS/kqa/library/cdr/CDRouterLibrary.py
Library    /home/ats/ATS/kqa/library/terminal/DeviceTerminal.py
Library    /home/ats/ATS/kqa/library/utils/TableVerificationLibrary.py

*** Variables ***
${PACKAGE_NAME}    QA/PG6692G/DS-LITE
${VERIFY_INFO}     SEPARATOR=${EMPTY}
...
...    | Name                  | Configuration         | \n
...    | QA/PG6692G/DS-LITE    | QA-PG6692G-DS-LITE    | \n

*** Test Cases ***
Run CDR Test
    [Setup]    Test Setup

    Test Connection And Verify Package
    Launch Job And Check Status
    Check Result From CDR

*** Keywords ***
Establish Connection
    [Arguments]            ${device_name}
    ${cdrouter_info}       Get Device Info    ${device_name}
    Set Test Variable      ${CDR_PATH}        ${cdrouter_info['connections']['path']}
    Set Test Variable      ${CDR_USERNAME}    ${cdrouter_info['custom']['username']}
    Set Test Variable      ${CDR_PASSWORD}    ${cdrouter_info['custom']['password']}
    Connect To Cdrouter    ${CDR_PATH}        ${CDR_USERNAME}                            ${CDR_PASSWORD}

Test Connection And Verify Package
    Establish Connection    CDRouter
    ${package}              Get Package By Name         ${PACKAGE_NAME}
    ${package_info}         Get Package Info By Name    ${PACKAGE_NAME}

    ${package_info}    Create Table    ${package_info}
    ${veriry_table}    Create Table    ${VERIFY_INFO}

    ${result}         Verify Table    ${veriry_table}    ${package_info}    whitelist
    Should Be True    ${result}

Launch Job And Check Status
    ${package_id}                          Get Package Id By Name       ${PACKAGE_NAME}
    ${job_id}                              Set Launch Job               ${package_id}
    Run Keyword And Continue On Failure    Check Until Job Completed    ${job_id}
    ${result_id}                           Get Result Id From Job       ${job_id}
    Set Test Variable                      ${result_id}

Check Result From CDR
    ${result}                Get Result By Id    ${result_id}
    # Log To Console           ${result}
    # ${msg}                   ${status}           Get Result Msg    ${result_id}
    Check Is Error Result    ${result_id}

Test Setup
    Load Topology    /home/ats/ATS/kqa/suites_data/topology.yaml