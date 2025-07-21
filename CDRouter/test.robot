*** Settings ***
Library        library.CustomKeywords    WITH NAME    CustomKeywords
Suite Setup    Setup Common

*** Variables ***
${CDR_PACKAGE_NAME}    QA/General/IPv4(DHCP)_TRONG
${CDR_CONFIG_NAME}     [QA]PG6692G-General-IPv4(DHCP)
${CDR_DEVICE_NAME}     [QA]Alpha/PG6692G/KAON1A154B58(newHW)
@{IDS_LIST}            20250514094343                           20250514102230

*** Test Cases ***
Test Get Result
    Get CDRouter Info
    Connect To CDRouter    ${CDR_PATH}    ${USER}    ${PASS}
    # Get Diff Test Item      ${IDS_LIST}
    # Get List Test Result    20250514102230
    # ${file_path}            Export Test Detail To CSV    20250514102230
    # Log To Console          File path: ${file_path}

    ${id_last}        Get Latest Result Id            ${CDR_PACKAGE_NAME}
    Log To Console    Latest result ID: ${id_last}

*** Keywords ***
Get CDRouter Info
    ${USER}               Get Device Custom Field        Cdr0    username
    ${PASS}               Get Device Custom Field        Cdr0    password
    Set Suite Variable    ${USER}
    Set Suite Variable    ${PASS}
    ${CDR_PATH}           Get Device Connection Field    Cdr0    path
    Set Suite Variable    ${CDR_PATH}

Setup Common
    Load Topology    /home/ats/ATS/kqa/CDRouter/topology.yaml
