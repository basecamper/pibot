class CallControls {

    constructor() {
        this.name = "Call"
        this.iCall = create_element("input",{type:"text", value:"", size:20});
        var iCall = iCall;
        this.bAcceptCall = create_element("div",{className:"button", innerHTML:"accept", onclick:function(e) {
            print("You're accepting the call");
            socket.send("phone,A");
        }});
        this.bCancelCall = create_element("div",{className:"button", innerHTML:"cancel", onclick:function(e) {
            print("You're canceling the call");
            socket.send("phone,H");
        }});
        this.bForwardCall = create_element("div",{className:"button", innerHTML:"forward", onclick:function(e) {
            print("Forwarding the call to \""+iCall.value+"\"");
            socket.send("phone,TODO"+iCall.value);
        }});
        this.bDialCall = create_element("div",{className:"button", innerHTML:"dial", onclick:function(e) {
            print("Dialing to \""+iCall.value+"\"");
            socket.send("phone,D"+iCall.value);
        }});
        var bMute;
        this.bMute = create_element("div",{className:"button", innerHTML:"mute", onclick:function(e) {
            if (bMute.innerHTML == "mute") {
                print("Muting");
                socket.send("phone,+CMUT=1");
                bMute.innerHTML == "unmute";
            } else {
                print("Unmuting");
                socket.send("phone,+CMUT=0");
                bMute.innerHTML == "mute";
            }
        }});
        bMute = this.bMute;

        this.container = create_element("div", {className:"container hidden", id:"callContainer"});
        this.container.appendChild( createLabel("Call") );
        this.container.appendChild(this.bAcceptCall);
        this.container.appendChild(this.bCancelCall);
        this.container.appendChild( create_placeholder() );
        this.container.appendChild(this.bMute);
        this.container.appendChild( create_placeholder() );
        this.container.appendChild(this.iCall);
        this.container.appendChild(this.bDialCall);
        //this.container.appendChild(this.bForwardCall);
    }
}