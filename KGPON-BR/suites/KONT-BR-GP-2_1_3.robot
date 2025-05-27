*** Settings ***
Resource    /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***


*** Test Cases ***
Emergency Onu O7 Active
    [Teardown]               Close Connection
    Connect To Huawei
    ${log}                   Read Until Prompt
    Access Config Mode
    Access Interface Mode
    ${onu_id}                Get Onuid From Serial    ${OLT_PON_INDEX}    ${ONU_SN}
    Go To Previous Mode
    Access Diagnose Mode

    Send Command                             anti-rogueont isolate ${OLT_PON_ALIAS}/${OLT_PON_INDEX} ${onu_id}
    Sleep                                    10s
    ${log}                                   Read Until Prompt
    Log To Console                           ${log}
    Create Alarm Message Verify O7 Active
    Should Match Regexp                      ${log}                                                               ${alarm_message}


# Emergency Onu O7 Deactive
#    [Teardown]                                 Close Connection
#    Connect To Huawei
#    Access Config Mode
#    Access Interface Mode
#    ${onu_id}                                  Get Onuid From Serial                                                     ${OLT_PON_INDEX}    ${ONU_SN}
#    Go To Previous Mode
#    Access Diagnose Mode
#    Send Command                               undo anti-rogueont isolate ${OLT_PON_ALIAS}/${OLT_PON_INDEX} ${onu_id}
#    Sleep                                      15s
#    ${log}                                     Read Until Prompt
#    Log To Console                             ${log}
#    Create Alarm Message Verify O7 Deactive
#    Should Match Regexp                        ${log}                                                                    ${alarm_message}



*** Keywords ***
Create Alarm Message Verify O7 Active
    Set Variable    ${alarm_message}
    ...             ALARM NAME\s*:\s*The feeder fiber is broken or OLT can not receive any expected optical signals\(LOS\)[\r\n]+PARAMETERS\s*:\s*FrameID:\s*\d+,\s*SlotID:\s*\d+,\s*PortID:\s*${OLT_PON_INDEX},\s*The number of affected ONTs:\s*${onu_id}

Create Alarm Message Verify O7 Deactive
    Set Variable    ${alarm_message}
    ...             ALARM NAME\s*:\s*OLT can receive expected optical signals from ONTs\(LOS recovers\)[\r\n]+PARAMETERS\s*:\s*FrameID:\s*\d+,\s*SlotID:\s*\d+,\s*PortID:\s*${OLT_PON_INDEX}
