*** Settings ***
Library     SeleniumLibrary
Library     Collections
Library     String
Resource    /home/ats/ATS/kqa/PG2142_Web/suites/common/keyword.resource

*** Variables ***
${URL}                     https://34.1.1.107
${USERNAME}                admin
${PASSWORD}                admin
${BROWSER}                 chrome
${FIRMWARE_FILE}           PG2142_Millicom_4.0.19_rev728.e
${PATH}                    /home/ats/ATS/kqa/PG2142_Web/PG2142_Millicom_4.0.19_rev728.e
${FIRMWARE_VERSION_OLD}    4.0.18D
${FIRMWARE_VERSION_NEW}    4.0.19

*** Test Cases ***
Upgrade Firmware Via Web
    [Teardown]                 Close All Browsers
    [Setup]                    Login Web                  ${BROWSER}          ${URL}    ${USERNAME}    ${PASSWORD}
    Check current version      ${FIRMWARE_VERSION_OLD}
    Upgrade Firmware Action    ${PATH}                    ${FIRMWARE_FILE}

*** Keywords ***
Check current version
    [Arguments]    ${VERSION}

    Open Menu And Go To Page         management                                          firmware-upgrade
    Wait Until Element Is Visible    xpath=//div[contains(@id, 'divVersion')]//strong
    ${current_version_raw}           Get Text                                            xpath=//div[contains(@id, 'divVersion')]//strong
    ${current_version}               Get Regexp Matches                                  ${current_version_raw}                              [0-9.]+[A-Z]?
    Log To Console                   ${current_version}[0]
    Should Be Equal As Strings       ${current_version}[0]                               ${VERSION}

Upgrade Firmware Action
    [Arguments]                      ${path_file}                                      ${file_name}                                
    Choose File                      xpath=//input[contains(@class, 'input--file')]    ${path_file}
    Wait Until Element Is Visible    xpath=//p[contains(@id, 'fileSelected')]
    ${file_loader}                   Get Text                                          xpath=//p[contains(@id, 'fileSelected')]
    ${file_loader}                   Replace String                                    ${file_loader}                              Remove    ${EMPTY}
    Log To Console                   ${file_loader}
    Should Be Equal As Strings       ${file_loader}                                    ${file_name}

    Click Element                    xpath=//label[contains(@class, 'btn btn--primary') and contains(text(), 'Install')]
    Wait Until Element Is Visible    xpath=//label[contains(@class, 'btn btn--primary') and contains(text(), 'Installing')]

    Sleep                          200s
    Wait Until Keyword Succeeds    5x      10s    Login Web    ${BROWSER}    ${URL}    ${USERNAME}    ${PASSWORD}

    Check current version    ${FIRMWARE_VERSION_NEW}

