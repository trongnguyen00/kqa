*** Settings ***
Resource    /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***


*** Test Cases ***
Emergency Onu O7 Active
    [Teardown]    Run Keywords    Send Command    undo anti-rogueont isolate ${OLT_PON_ALIAS}/${OLT_PON_INDEX} ${onu_id}    AND    Close Connection

    Connect To Huawei
    Access Config Mode
    Access Interface Mode
    ${onu_id}                Get Onuid From Serial    ${OLT_PON_INDEX}    ${ONU_SN}
    Set Test Variable        ${onu_id}
    Go To Previous Mode
    Access Diagnose Mode

    Send Command    anti-rogueont isolate ${OLT_PON_ALIAS}/${OLT_PON_INDEX} ${onu_id}
    Sleep           10s

    Wait Until Keyword Succeeds    5x    5s    Check The Alarm Message

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
    Set Test Variable    ${alarm_message}    ALARM NAME :The feeder fiber is broken or OLT can not receive any expected
    Set Test Variable    ${info}             PARAMETERS :FrameID: 0, SlotID: 2, PortID: 6


Check The Alarm Message
    ${log}                                   Read
    Log To Console                           ${log}
    Create Alarm Message Verify O7 Active
    Should Contain                           ${log}    ${alarm_message}
    Should Contain                           ${log}    ${info}