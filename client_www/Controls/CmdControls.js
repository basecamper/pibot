

class CmdControls {
    constructor() {
        this.name = "Cmd"
        var iMessage =  create_element("input",{type:"text", value:"phone,+CSQ",
        onkeydown:function(e) {
            if (e.keyCode == 13)
            socket.send(iMessage.value);
        }});
        this.bSend = create_element("div",{className:"button", innerHTML:"send", onclick:function(e) {
            print("Sending: \"" + iMessage.value+"\"");
            socket.send(iMessage.value);
        }});

        this.bClock = create_element("div",{className:"button", innerHTML:"clock",
            onclick:function(e) {
                print("Asking for clock");
                socket.send("phone,+CCLK?");
            }
        });
        this.bStatus = create_element("div",{className:"button", innerHTML:"status", onclick:function(e) {
            print("Asking for status");
            socket.send("phone,+CSQ;+CBC");
        }});
        this.container= create_element("div", {className:"container hidden", id:"cmdContainer"});
        
        this.container.appendChild( createLabel("Cmd") );
        this.container.appendChild( iMessage);
        this.container.appendChild( this.bSend);
        this.container.appendChild( create_placeholder() );
        this.container.appendChild( this.bClock);
        this.container.appendChild( this.bStatus);
    
    }
}