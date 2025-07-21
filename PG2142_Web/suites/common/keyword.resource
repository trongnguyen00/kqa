*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Keywords ***
Login Web
    [Arguments]    ${BROWSER}    ${URL}    ${USERNAME}    ${PASSWORD}

    Close All Browsers
    Open Browser                     browser=${BROWSER}    options=add_argument("--disable-popup-blocking"); add_argument("--ignore-certificate-errors"); add_argument("--headless"); add_argument("--no-sandbox"); add_argument("--disable-dev-shm-usage")
    Go To                            ${URL}
    Title Should Be                  KAON Broadband CPE
    Wait Until Element Is Visible    name=username_in
    Input Text                       name=username_in      ${USERNAME}
    Input Text                       name=password_in      ${PASSWORD}
    Click Button                     name=submit
    Sleep                            5s

Open Menu And Go To Page
    [Arguments]    ${menu_label}    ${page_label}

    Click Element                    class=hamburger
    Wait Until Element Is Visible    css:span.nav__link__label[data-args="${menu_label}"]
    Click Element                    css:span.nav__link__label[data-args="${menu_label}"]
    Wait Until Element Is Visible    css:span.nav__link__label[data-args="${page_label}"]
    Click Element                    css:span.nav__link__label[data-args="${page_label}"]
    Wait Until Element Is Visible    xpath=//li[contains(@data-value, "${menu_label}")]//a[contains(@class, "nav__sublink active")]//span[contains(@data-args, "${page_label}")]
