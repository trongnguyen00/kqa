*** Settings ***
Library     SeleniumLibrary
Library     Collections
Library     String
Resource    /home/ats/ATS/kqa/PG2142_Web/suites/common/keyword.resource

*** Variables ***
${URL}         https://34.1.1.107
${USERNAME}    admin
${PASSWORD}    admin
${BROWSER}     chrome

${wan_interface}    veip0.2
${rule_name}        testqqq
${ip_external}      2.2.2.2
${port_external}    5060
${ip_internal}      192.168.1.55
${port_internal}    5060
${protocol}         TCP+UDP


*** Test Cases ***
Set Port Forwarding Rule
    [Teardown]             Close All Browsers
    [Setup]                Login Web             ${BROWSER}    ${URL}    ${USERNAME}    ${PASSWORD}
    Create Rule
    Verify Rule Created

*** Keywords ***
Create Rule
    Open Menu And Go To Page    advanced    port-forwarding

    Wait Until Element Is Visible    xpath=//h1[contains(@class, 'page__title') and contains(text(), 'Port Forwarding')]
    Click Button                     id=btnAddRule
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'add_rule')]//h1[contains(@id, 'action_title')]
    Input Text                       xpath=//input[contains(@id, 'name_rule')]
    ...                              ${rule_name}

    Click Element                    xpath=//div[contains(@name, 'src-network')]//span[contains(@class, 'ivu-select-placeholder')]
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'src-network')]//div[contains(@class, 'ivu-select-visible')]
    ${wan_interface}                 Get Text
    ...                              xpath=//div[contains(@name, 'src-network')]//div[contains(@class, 'ivu-select-visible')]//ul[contains(@class, 'ivu-select-dropdown-list')]
    Log To Console                   ${wan_interface}
    Click Element                    xpath=//div[contains(@name, 'src-network')]//div[contains(@class, 'ivu-select-visible')]//ul[contains(@class, 'ivu-select-dropdown-list')]//li[contains(text(), '${wan_interface}')]
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'src-network')]//span[contains(@class, 'ivu-select-placeholder') and contains(text(), '${wan_interface}')]

    Click Element                    xpath=//div[contains(@name, 'src-ip')]//span[contains(@class, 'ivu-select-placeholder')]
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'src-ip')]//div[contains(@class, 'ivu-select-visible')]
    Click Element                    xpath=//div[contains(@name, 'src-ip')]//div[contains(@class, 'ivu-select-visible')]//ul[contains(@class, 'ivu-select-dropdown-list')]//li[contains(text(), 'Custom IP')]
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'src-ip')]//span[contains(@class, 'ivu-select-placeholder') and contains(text(), 'Custom IP')]
    Input Text                       xpath=//div[contains(@name, 'src-ip')]//input[contains(@id, 'custom_external_ip')]
    ...                              ${ip_external}

    Click Element                    xpath=//div[contains(@name, 'external-port')]//span[contains(@class, 'ivu-select-placeholder')]
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'external-port')]//div[contains(@class, 'ivu-select-visible')]
    Click Element                    xpath=//div[contains(@name, 'external-port')]//ul[contains(@class, 'ivu-select-dropdown-list')]//li[contains(text(), 'Custom port')]
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'external-port')]//span[contains(@class, 'ivu-select-placeholder') and contains(text(), 'Custom port')]
    Input Text                       xpath=//div[contains(@name, 'external-port')]//input[contains(@id, 'custom_external_port')]
    ...                              ${port_external}

    Click Element                    xpath=//div[contains(@name, 'dest-ip')]//span[contains(@class, 'ivu-select-placeholder')]
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'dest-ip')]//div[contains(@class, 'ivu-select-visible')]
    Click Element                    xpath=//div[contains(@name, 'dest-ip')]//ul[contains(@class, 'ivu-select-dropdown-list')]//li[contains(text(), 'Custom IP')]
    Input Text                       xpath=//div[contains(@name, 'dest-ip')]//input[contains(@id, 'custom_internal_ip')]
    ...                              ${ip_internal}


    Click Element                    xpath=//div[contains(@name, 'dest-port')]//span[contains(@class, 'ivu-select-placeholder')]
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'dest-port')]//div[contains(@class, 'ivu-select-visible')]
    Click Element                    xpath=//div[contains(@name, 'dest-port')]//div[contains(@class, 'ivu-select-visible')]//ul[contains(@class, 'ivu-select-dropdown-list')]//li[contains(text(), 'Custom port')]
    Input Text                       xpath=//div[contains(@name, 'dest-port')]//input[contains(@id, 'custom_internal_port')]
    ...                              ${port_internal}

    Click Element                    xpath=//div[contains(@name, 'protocol')]//span[contains(@class, 'ivu-select-placeholder')]
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'protocol')]//div[contains(@class, 'ivu-select-visible')]
    Click Element                    xpath=//div[contains(@name, 'protocol')]//ul[contains(@class, 'ivu-select-dropdown-list')]//li[contains(text(), '${protocol}')]

    Page Should Contain Button    xpath=//button[contains(@type, 'submit')]
    Click Element                 xpath=//button[contains(@type, 'submit')]

Verify Rule Created
    Wait Until Element Is Visible    xpath=//div[contains(@class, 'table')]//div[contains(@class, 'td') and contains(text(), '${rule_name}')]    timeout=10s

    Element Should Be Visible    xpath=//div[contains(@class, 'table')]//button[contains(@class, btn--primary) and contains(@value, '1|${rule_name}|${wan_interface}|${ip_external}|${ip_internal}|${port_external}|${port_external}|TCP or UDP|${port_internal}|${port_internal}')]


