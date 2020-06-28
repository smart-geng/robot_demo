from .. import soap


def make_request_transfercomplete(
        start_time : str ,
        end_time : str ,
        CommandKey : str
) -> str:
    return soap.soapify(f"""
       <cwmp:TransferComplete>
        <CommandKey>{CommandKey}</CommandKey>
        <FaultStruct>
         <FaultCode>0</FaultCode>
         <FaultString></FaultString>
        </FaultStruct>
        <StartTime>{start_time}</StartTime>
        <CompleteTime>{end_time}</CompleteTime>
       </cwmp:TransferComplete>
    """)
