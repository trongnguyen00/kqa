*** Settings ***
Resource    /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***


*** Test Cases ***
Automatic Ont Discovery
    Connect To Huawei
    Access Config Mode
    Access Interface Mode
    ${onu_id}                Get Onuid From Serial    ${OLT_PON_INDEX}      ${ONU_SN}
    ${find_onu}              Get Onu Info             ${OLT_PON_INDEX}       ${onu_id}
    ${find_onu_table}        Parse Table              ${find_onu}            /home/ats/ATS/kqa/KGPON-BR/suites/resource/onu_info_hw.template
    Create Onu Info Table
    ${result}                Verify Table             ${onu_verify_table}    ${find_onu_table}
    Should Be True           ${result}

*** Keywords ***
Create Onu Info Table
    ${onu_info}    Catenate
    ...            | PORT                                 | SN           | CONTROL_FLAG    | RUN_STATE    | CONFIG_STATE    | MATCH_STATE    | \n
    ...            | ${OLT_PON_ALIAS}/${OLT_PON_INDEX}    | ${ONU_SN}    | active          | online       | normal          | match          | \n

    ${onu_verify_table}    Create Table           ${onu_info}
    Set Test Variable      ${onu_verify_table}