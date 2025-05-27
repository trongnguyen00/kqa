*** Settings ***
Resource    /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***


*** Test Cases ***
Automatic Ont Discovery
    Connect To Huawei
    ${find_onu}            Get Onu Unprovision
    ${find_onu_table}      Parse Table            ${find_onu}            /home/ats/ATS/kqa/KGPON-BR/suites/resource/unprovision_onu_hw.template
    ${onu_verify_table}    Create Table           ${onu_verify}
    Log To Console         ${find_onu_table}
    Log To Console         ${onu_verify_table}
    ${result}              Verify Table           ${onu_verify_table}    ${find_onu_table}
    Should Be True         ${result}

*** Keywords ***
