class SmsControls {
    constructor() {
        this.name = "Sms"

        var iChset = create_element("input",{id:"smsSendChset", type:"text", placeholder:"charset", value:"8859-1", size:8});
        var bSendChset = create_element("div",{className:"button", innerHTML:"set", onclick:function(e) {
            print("Sending chset:",iChset.value );
            socket.send("phone,+CSCS=\""+iChset.value+"\"");
        }});
        
        var iSmsVerboseOn = create_element("input",{id:"verboseSmsOn", name:"smsVerbose", type:"checkbox", value:"on", checked:"checked"});
        var bSmsVerbose = create_element("div",{className:"button", innerHTML:"verbosity", onclick:function(e) {
            print("Setting sms verbosity:");
            let n = 0;
            if (iSmsVerboseOn.checked) {
                n = 1;
            }
            socket.send("phone,+CSDH="+n);
        }});
        var iSmsReadId = create_element("input",{id:"readSmsId", type:"text", placeholder:"id", size:3});
        var bSmsReadId = create_element("div",{className:"button", innerHTML:"read", onclick:function(e) {
            let id = iSmsReadId.value;
            print("Requesting sms "+id+":");
            socket.send("phone,+CMGR="+id);
        }});
        var bSmsReadUnread = create_element("div",{className:"button", innerHTML:"unread", onclick:function(e) {
            print("Requesting unread sms:");
            socket.send("phone,+CMGL=\"REC UNREAD\"");
        }});
        
        var bSmsReadAll = create_element("div",{className:"button", innerHTML:"all", onclick:function(e) {
            print("Requesting all sms:");
            socket.send("phone,+CMGL=\"ALL\"");
        }});

        this.iSmsSendEntry = create_element("input",{id:"smsSendNum", type:"text", placeholder:"number", value:"", size:20});
        var iSmsSendEntry = this.iSmsSendEntry;
        
        var iSmsSendText = create_element("input",{id:"smsSendText", type:"text", placeholder:"txt", size:40});
        var bSmsSend = create_element("div",{className:"button", innerHTML:"send", onclick:function(e) {
            print("Sending sms");
            socket.send("phone,+CMGS=\""+iSmsSendEntry.value+"\"\n"+iSmsSendText.value +"\n"+ String.fromCharCode(26));
        }});
        
        var iSmsDeleteNum = create_element("input",{id:"deleteSmsNum", type:"text", placeholder:"id", size:3});
        var bSmsDeleteAll = create_element("div",{className:"button", innerHTML:"all", onclick:function(e) {
            print("Deleting all sms");
            socket.send("phone,+CMGDA=\"DEL READ\"");
        }});
        var bSmsDeleteNum = create_element("div",{className:"button", innerHTML:"delete:", onclick:function(e) {
            print("Deleting sms:");
            var num = iSmsDeleteNum.value;
            socket.send("phone,+CMGD="+num+",0");
        }});
        
        this.container = create_element("div", {className:"container hidden", id:"smsContainer"}); 
        
        this.container.appendChild( createLabel("Sms") );
        this.container.appendChild( iChset );
        this.container.appendChild( bSendChset );
        this.container.appendChild( create_placeholder() );
        this.container.appendChild( bSmsVerbose );
        this.container.appendChild( iSmsVerboseOn );
        this.container.appendChild( create_placeholder() );
        this.container.appendChild( bSmsReadId );
        this.container.appendChild( iSmsReadId );
        this.container.appendChild( bSmsReadUnread );
        this.container.appendChild( bSmsReadAll );
        this.container.appendChild( create_placeholder() );
        this.container.appendChild( this.iSmsSendEntry );
        this.container.appendChild( iSmsSendText );
        this.container.appendChild( bSmsSend );
        this.container.appendChild( create_placeholder() );
        this.container.appendChild( bSmsDeleteNum );
        this.container.appendChild( iSmsDeleteNum );
        this.container.appendChild( create_placeholder("or") );
        this.container.appendChild( bSmsDeleteAll );
    }
}

