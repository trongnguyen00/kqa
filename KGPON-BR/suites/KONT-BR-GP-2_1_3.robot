*** Settings ***
Resource    /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***


*** Test Cases ***
Emergency Onu O7
    [Teardown]    Run Keywords    Send Command    undo anti-rogueont isolate ${OLT_PON_ALIAS}/${OLT_PON_INDEX} ${ONU_ID}   AND    Sleep    5s    AND    Close Connection

    Connect To Huawei
    Access Config Mode
    Access Interface Mode
    Get Onu Id
    Go To Previous Mode
    Access Diagnose Mode

    Send Command                   anti-rogueont isolate ${OLT_PON_ALIAS}/${OLT_PON_INDEX} ${ONU_ID}
    Wait Until Keyword Succeeds    5x                                                                   10s    Check The Alarm Active Message
    Sleep                          15s

    Send Command                   undo anti-rogueont isolate ${OLT_PON_ALIAS}/${OLT_PON_INDEX} ${ONU_ID}
    Wait Until Keyword Succeeds    5x                                                                        10s    Check The Alarm Deactive Message


*** Keywords ***
Create Alarm Message Verify O7 Active
    Set Test Variable    ${alarm_message}    ALARM NAME :The feeder fiber is broken or OLT can not receive any expected
    Set Test Variable    ${info}             PARAMETERS :FrameID: 0, SlotID: 2, PortID: ${OLT_PON_INDEX}

Create Alarm Message Verify O7 Deactive
    Set Test Variable    ${alarm_message}    ALARM NAME :OLT can receive expected optical signals from ONTs
    Set Test Variable    ${info}             PARAMETERS :FrameID: 0, SlotID: 2, PortID: ${OLT_PON_INDEX}

Check The Alarm Active Message
    ${log}                                   Read
    Log To Console                           ${log}
    Create Alarm Message Verify O7 Active
    Should Contain                           ${log}    ${alarm_message}
    Should Contain                           ${log}    ${info}

Check The Alarm Deactive Message
    ${log}                                     Read
    Log To Console                             ${log}
    Create Alarm Message Verify O7 Deactive
    Should Contain                             ${log}    ${alarm_message}
    Should Contain                             ${log}    ${info}