*** Settings ***
Resource    /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***


*** Test Cases ***
Ont Optical Verification
    [Teardown]                Set State Onu Uni Up    ${OLT_PON_INDEX}    ${ONU_ID}           ${ONU_UNI_ALIAS}
    Connect To Huawei
    Access Config Mode
    Access Interface Mode
    Get Onu Id
    Verify Onu Uni State      up
    Set State Onu Uni Down    ${OLT_PON_INDEX}        ${ONU_ID}           ${ONU_UNI_ALIAS}
    Sleep                     5s
    Verify Onu Uni State      down
    Sleep                     5s
    Set State Onu Uni Up      ${OLT_PON_INDEX}        ${ONU_ID}           ${ONU_UNI_ALIAS}
    Sleep                     5s
    Verify Onu Uni State      up

*** Keywords ***
Verify Onu Uni State
    [Arguments]          ${onu_uni_state}
    ${onu_uni_verify}    Catenate
    ...                  | ONU_ID            | PORT_ID             | LINK_STATE          | \n
    ...                  | ${ONU_ID}         | ${ONU_UNI_ALIAS}    | ${onu_uni_state}    | \n

    ${onu_verify_table}    Create Table        ${onu_uni_verify}
    ${onu_uni_info}        Get Onu Uni Info    ${OLT_PON_INDEX}       ${ONU_ID}
    Log To Console         ${onu_uni_info}
    ${onu_uni_table}       Parse Table         ${onu_uni_info}        /home/ats/ATS/kqa/KGPON-BR/suites/resource/parse_ont_uni_status.template
    ${result}              Verify Table        ${onu_verify_table}    ${onu_uni_table}
    Should Be True         ${result}

