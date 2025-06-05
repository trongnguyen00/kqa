*** Settings ***
Resource    /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***


*** Test Cases ***
Manage Onu Version Via Omci
    [Teardown]
    Connect To Huawei
    Access Config Mode
    Access Interface Mode
    Get Onu Id
    Verify Onu Version
    Change Os Onu

*** Keywords ***
# Get Onu Version Via Omci
#    ${version_onu}      Get Onu Version     ${OLT_PON_INDEX}    ${ONU_ID}
#    ${onu_ver_table}    Parse Table         ${version_onu}      /home/ats/ATS/kqa/KGPON-BR/suites/resource/parse_ont_version.template
#    RETURN              ${onu_ver_table}

# # Get Onu Version Via Console
# #    [Teardown]             Close Connection
# #    Connect To Dut         Onu0
# #    ${actual_rlt}          Send Command           sw_info
# #    ${actual_rlt_table}    Parse Table            ${actual_rlt}    /home/ats/ATS/kqa/library/terminal/dal/template/ont_console_version.template
# #    RETURN                 ${actual_rlt_table}

# Verify Onu Version
#    ${onu_ver_omci}    Get Onu Version Via Omci
#    ${onu_ver_cs}      Get Onu Version Via Console
#    ${result}          Verify Table                   ${onu_ver_cs}    ${onu_ver_omci}
#    Should Be True     ${result}

Change Os Onu
    Switch Os Onu                  olt0-pon0    ${ONU_ID}
    Sleep                          150s
    Wait Until Keyword Succeeds    5x           10s          Check ONT Activation Status
    Verify Onu Version