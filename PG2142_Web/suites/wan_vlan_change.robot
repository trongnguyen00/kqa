*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${URL}         https://34.1.1.107
${USERNAME}    admin
${PASSWORD}    admin
${BROWSER}     chrome
${VLAN_ID}     1000

*** Test Cases ***
Change WAN VLAN
    [Teardown]         Close All Browsers
    Login Web
    Sleep              5s
    Change WAN VLAN


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

Change WAN VLAN
    Click Element                    class=hamburger
    Wait Until Element Is Visible    css:span.nav__link__label[data-args="network"]
    Click Element                    css:span.nav__link__label[data-args="network"]
    Click Element                    css:span.nav__link__label[data-args="multiwan"]

    Wait Until Element Is Visible    xpath=//button[contains(@data-value, '"service-desc":"IPTV"')]
    Click Element                    xpath=//button[contains(@data-value, '"service-desc":"IPTV"')]

    Wait Until Element Is Visible    xpath=//div[contains(@name, 'vid')]
    ${vid_field}                     Get WebElement                                xpath=//div[contains(@name, 'vid')]
    Input Text                       xpath=//div[contains(@name, 'vid')]//input    ${VLAN_ID}
    Click Button                     id=btnSaveEdit

    Wait Until Element Is Not Visible    xpath=//div[contains(@class, 'action_section')]//div[contains(@class, 'modal')]//div[contains(@class, 'modal__window')]

    Wait Until Element Is Visible    xpath=//button[contains(@data-value, '"service-desc":"IPTV"')]    timeout=10s

    ${elements}    Get WebElements    xpath=//div[contains(@id, 'wan_vid')]//div[contains(@class, 'ctable__cell')]

    ${vlan_ids}       Create List
    FOR               ${element}     IN            @{elements}
    ${vlan_id}        Get Text       ${element}
    Append To List    ${vlan_ids}    ${vlan_id}
    END
    Should Contain    ${vlan_ids}    ${VLAN_ID}