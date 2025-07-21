*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${URL}         https://34.1.1.107
${USERNAME}    admin
${PASSWORD}    admin
${BROWSER}     chrome
${VLAN_ID}     1000
${WAN_NAME}    HSI
${WAN_MODE}    IPoE

*** Test Cases ***
Change WAN Mode
    [Teardown]         Close All Browsers
    [Setup]            Login Web
    Change WAN Mode

*** Keywords ***
Login Web
    Close All Browsers
    Open Browser                     browser=${BROWSER}    options=add_argument("--disable-popup-blocking"); add_argument("--ignore-certificate-errors"); add_argument("--headless"); add_argument("--no-sandbox"); add_argument("--disable-dev-shm-usage")
    Go To                            ${URL}
    Title Should Be                  KAON Broadband CPE
    Wait Until Element Is Visible    name=username_in
    Input Text                       name=username_in      ${USERNAME}
    Input Text                       name=password_in      ${PASSWORD}
    Click Button                     name=submit
    Sleep                            5s

Change WAN Mode
    Click Element                    class=hamburger
    Wait Until Element Is Visible    css:span.nav__link__label[data-args="network"]
    Click Element                    css:span.nav__link__label[data-args="network"]
    Click Element                    css:span.nav__link__label[data-args="multiwan"]

    Wait Until Element Is Visible    xpath=//button[contains(@data-value, '"service-desc":"${WAN_NAME}"')]
    Click Element                    xpath=//button[contains(@data-value, '"service-desc":"${WAN_NAME}"')]

    Wait Until Element Is Visible    xpath=//div[contains(@name, 'service_type')]
    Click Element                    xpath=//div[contains(@name, 'service_type')]//span[contains(@class, 'ivu-select-placeholder')]
    Wait Until Element Is Visible    xpath=//div[contains(@name, 'service_type')]//div[contains(@class, 'ivu-select-visible')]
    Click Element                    xpath=//div[contains(@name, 'service_type')]//ul[contains(@class, ivu-select-dropdown)]//li[contains(@class, 'ivu-select-item') and contains(text(), '${WAN_MODE}')]

    Wait Until Element Is Visible    xpath=//div[contains(@name, 'service_type')]//span[contains(@class, 'ivu-select-placeholder') and contains(text(), '${WAN_MODE}')]

    Click Button                         id=btnSaveEdit
    Wait Until Element Is Not Visible    xpath=//div[contains(@class, 'action_section')]//div[contains(@class, 'modal')]//div[contains(@class, 'modal__window')]

    Wait Until Element Is Visible    xpath=//button[contains(@data-value, '"service-desc":"${WAN_NAME}"')]    timeout=10s

    # ${elements}    Get WebElements    xpath=//div[contains(@id, 'wan_vid')]//div[contains(@class, 'ctable__cell')]

