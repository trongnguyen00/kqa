*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}         https://34.1.1.107
${USERNAME}    admin
${PASSWORD}    admin
${BROWSER}     chrome

*** Test Cases ***
Login Test

    Close All Browsers
    Open Browser          browser=${BROWSER}    options=add_argument("--disable-popup-blocking"); add_argument("--ignore-certificate-errors"); add_argument("--headless"); add_argument("--no-sandbox"); add_argument("--disable-dev-shm-usage")
    Go To                 ${URL}
    Title Should Be       KAON Broadband CPE
    Close Browser
