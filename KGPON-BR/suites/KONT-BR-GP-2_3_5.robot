*** Settings ***
Documentation    Manage ONU IP host information via OMCI commands. Note: Configure dhcp reservation for WAN ONT Iphost like Variableds ${IPHOST_IP}, ${IPHOST_MASK}, ${IPHOST_GW}...
Resource         /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***
${IPHOST_IP}           31.1.1.100
${IPHOST_STATIC_IP}    31.1.1.100
${IPHOST_MASK}         255.255.255.0
${IPHOST_GW}           31.1.1.254
${IPHOST_PRI_DNS}      1.1.1.1
${IPHOST_VLAN}         800
${IPHOST_PRIORITY}     5

*** Test Cases ***
Manage Onu Iphost Information
    [Teardown]               Set Iphost Dhcp
    Connect To Huawei
    Access Config Mode
    Access Interface Mode
    Get Onu Id
    Set Iphost Dhcp
    Sleep                    10s
    Verify Iphost Dynamic
    Set Iphost Static
    Sleep                    10s
    Verify Iphost Static

*** Keywords ***
Set Iphost Dhcp
    Send Command    ont ipconfig ${OLT_PON_INDEX} ${ONU_ID} dhcp vlan ${IPHOST_VLAN} priority ${IPHOST_PRIORITY}

Set Iphost Static
    Send Command    ont ipconfig ${OLT_PON_INDEX} ${ONU_ID} static ip-address ${IPHOST_STATIC_IP} mask ${IPHOST_MASK} gateway ${IPHOST_GW} vlan ${IPHOST_VLAN} pri-dns ${IPHOST_PRI_DNS}

Verify Iphost Dynamic
    ${iphost_info}          Get Onu Iphost Info    ${OLT_PON_INDEX}    ${ONU_ID}
    ${iphost_info_table}    Parse Table            ${iphost_info}      /home/ats/ATS/kqa/KGPON-BR/suites/resource/parse_ont_iphost.template

    ${verify_iphost}    Catenate
    ...                 | IP              | MASK              | GATEWAY         | DNS1                 | VLAN              | CONFIG_TYPE    | \n
    ...                 | ${IPHOST_IP}    | ${IPHOST_MASK}    | ${IPHOST_GW}    | ${IPHOST_PRI_DNS}    | ${IPHOST_VLAN}    | DHCP           | \n

    ${verify_iphost_table}    Create Table    ${verify_iphost}
    ${result}                 Verify Table    ${verify_iphost_table}    ${iphost_info_table}
    Should Be True            ${result}

Verify Iphost Static
    ${iphost_info}          Get Onu Iphost Info    ${OLT_PON_INDEX}    ${ONU_ID}
    ${iphost_info_table}    Parse Table            ${iphost_info}      /home/ats/ATS/kqa/KGPON-BR/suites/resource/parse_ont_iphost.template

    ${verify_iphost}    Catenate
    ...                 | IP                     | MASK              | GATEWAY         | DNS1                 | VLAN              | CONFIG_TYPE      | \n
    ...                 | ${IPHOST_STATIC_IP}    | ${IPHOST_MASK}    | ${IPHOST_GW}    | ${IPHOST_PRI_DNS}    | ${IPHOST_VLAN}    | Static config    | \n

    ${verify_iphost_table}    Create Table    ${verify_iphost}
    ${result}                 Verify Table    ${verify_iphost_table}    ${iphost_info_table}
    Should Be True            ${result}