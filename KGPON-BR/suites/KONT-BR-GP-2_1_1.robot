*** Settings ***
Resource    /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***
${ONU_VERIFY}    SEPARATOR=${EMPTY}
...
...    | PORT     | SN                  | VERSION       | MODEL     | \n
...    | 0/2/6    | 4B414F4EAF523D04    | 2.0.30_eng    | PM1191    | \n


*** Test Cases ***
Automatic Ont Discovery
    Connect To Huawei
    ${find_onu}            Get Onu Unprovision    Olt0                   olt0-pon0
    ${find_onu_table}      Parse Table            ${find_onu}            /home/ats/ATS/kqa/KGPON-BR/suites/resource/unprovision_onu_hw.template
    ${onu_verify_table}    Create Table           ${ONU_VERIFY}
    Log To Console       ${find_onu_table}
    Log To Console       ${onu_verify_table}
    ${result}              Verify Table           ${onu_verify_table}    ${find_onu_table}
    Should Be True         ${result}

*** Keywords ***
