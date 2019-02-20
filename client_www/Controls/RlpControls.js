

class RlpControls {
    constructor() {
        this.name = "Rlp"
        this.bRlpShow = create_element("div",{className:"button", innerHTML:"show", onclick:function(e) {
            print("Reading radio link protocol properties");
            socket.send("phone,+CRLP?");
        }});
        this.container= create_element("div", {className:"container hidden", id:"rlpContainer"});
        this.container.appendChild( createLabel("rlp:") );
        this.container.appendChild( this.bRlpShow );
    
    }
}