

class BandControls {
    constructor() {
        this.name = "Band"
        this.bBandShow = create_element("div",{className:"button", innerHTML:"show", onclick:function(e) {
            print("Reading current band");
            socket.send("phone,+CBAND?");
        }});
        this.bBandShowAll = create_element("div",{className:"button", innerHTML:"all", onclick:function(e) {
            print("Reading possible bands");
            socket.send("phone,+CBAND=?");
        }});
        var iBand = create_element("input",{type:"text", value:"DCS_MODE,ALL_BAND", size:20});
        this.bBandSet = create_element("div",{className:"button", innerHTML:"set", onclick:function(e) {
            print("Setting band "+iBand.value);
            socket.send("phone,+CBAND=\""+iBand.value+"\"");
        }});
        this.container= create_element("div", {className:"container hidden", id:"bandContainer"});
        
        this.container.appendChild( createLabel("band:") );
        this.container.appendChild( this.bBandShow );
        this.container.appendChild( this.bBandShowAll );
        this.container.appendChild( iBand );
        this.container.appendChild( this.bBandSet );
    
    }
}