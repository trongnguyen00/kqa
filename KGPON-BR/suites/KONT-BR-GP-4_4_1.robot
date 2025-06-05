*** Settings ***
Documentation    A TFTP Server is listening which is required for this test case.
Resource         /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***
${SERVER_TFTP}           192.168.150.103
${FW_NAME_UPGRADE}       PM1191_2.0.30_eng_616bcfa7_COMMON.s
${FW_ALIAS_UPGRADE}      2.0.30_eng
${FW_NAME_DOWNGRADE}     PM1191_2.0.29_eng_616bcfa7_COMMON.s
${FW_ALIAS_DOWNGRADE}    2.0.29_eng

*** Test Cases ***
Manage Firmware Upgrade And Downgrade Via Omci
    [Teardown]    Upgrade Firmware Via Omci

    Upgrade Firmware Via Omci
    Downgrade Firmware Via Omci

*** Keywords ***
Undo Upgrade Firmware Ont
    Send Command    undo ont-load select ${OLT_PON_ALIAS} ${OLT_PON_INDEX} ${ONU_ID}

Upgrade Firmware For Onu
    [Arguments]             ${fw_name}
    Go To Previous Mode
    Access Diagnose Mode
    Send Command            ont-load info program ${fw_name} tftp ${SERVER_TFTP}
    Send Command            ont-load select ${OLT_PON_ALIAS} ${OLT_PON_INDEX} ${ONU_ID}
    Send Command            ont-load start activemode immediate
    Sleep                   150s
    Go To Previous Mode

Verify Current Onu Version
    [Arguments]       ${version_alias}
    [Teardown]        Close Connection
    Connect To Dut    Onu0
    ${actual_rlt}     Send Command        sw_info
    Should Contain    ${actual_rlt}       ${version_alias}

Upgrade Firmware Via Omci
    [Teardown]    Run Keywords    Undo Upgrade Firmware Ont    AND    Close Connection

    Connect To Huawei
    Access Config Mode
    Access Interface Mode
    Check ONT Activation Status
    Verify Current Onu Version     ${FW_ALIAS_DOWNGRADE}
    Verify Onu Version
    # config mode
    Go To Previous Mode
    Upgrade Firmware For Onu       ${FW_NAME_UPGRADE}
    # enable mode
    Access Config Mode
    # Config mode
    Access Interface Mode
    # interface mode
    Wait Until Keyword Succeeds    10x                      10s    Check ONT Activation Status
    Verify Current Onu Version     ${FW_ALIAS_UPGRADE}
    Verify Onu Version

Downgrade Firmware Via Omci
    [Teardown]    Run Keywords    Undo Upgrade Firmware Ont    AND    Close Connection

    Connect To Huawei
    Access Config Mode
    Access Interface Mode
    Check ONT Activation Status
    Verify Current Onu Version     ${FW_ALIAS_UPGRADE}
    Verify Onu Version
    # config mode
    Go To Previous Mode
    Upgrade Firmware For Onu       ${FW_NAME_DOWNGRADE}
    # config mode
    Access Config Mode
    Access Interface Mode
    #interface mode
    Wait Until Keyword Succeeds    10x                      10s    Check ONT Activation Status
    Verify Current Onu Version     ${FW_ALIAS_DOWNGRADE}
    Verify Onu Version