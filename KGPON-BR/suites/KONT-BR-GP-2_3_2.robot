*** Settings ***
Resource    /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***


*** Test Cases ***
Ont Optical Verification
    Connect To Huawei
    Access Config Mode
    Access Interface Mode
    Check ONT Activation Status
    Get Value Of Optical
    Check Valid Optical

*** Keywords ***
Get Value Of Optical
    ${onu_optical_info}     Get Onu Optical Info    ${OLT_PON_INDEX}        ${ONU_ID}
    ${onu_optical_table}    Parse Table             ${onu_optical_info}     /home/ats/ATS/kqa/KGPON-BR/suites/resource/parse_ont_optic_info.template
    ${rx_power}             Get Value By Column     ${onu_optical_table}    RX_POWER
    ${tx_power}             Get Value By Column     ${onu_optical_table}    TX_POWER
    ${bias}                 Get Value By Column     ${onu_optical_table}    BIAS_CURRENT
    ${temperature}          Get Value By Column     ${onu_optical_table}    TEMPERATURE
    ${voltage}              Get Value By Column     ${onu_optical_table}    VOLTAGE
    ${rx_power}             Convert To Number       ${rx_power}
    ${tx_power}             Convert To Number       ${tx_power}
    ${bias}                 Convert To Number       ${bias}
    ${temperature}          Convert To Number       ${temperature}
    ${voltage}              Convert To Number       ${voltage}
    Set Test Variable       ${rx_power}
    Set Test Variable       ${tx_power}
    Set Test Variable       ${bias}
    Set Test Variable       ${temperature}
    Set Test Variable       ${voltage}

Check Valid Optical
    Should Be True    ${rx_power} >= -30.0 and ${rx_power} <= -8.0
    Should Be True    ${tx_power} >= 0 and ${tx_power} <= 7.0
    Should Be True    ${bias} >= 5 and ${bias} <= 60
    Should Be True    ${temperature} >= -40.0 and ${temperature} <= 85.0
    Should Be True    ${voltage} >= 3.0 and ${voltage} <= 3.5

