

class OpControls {
    constructor() {
        this.name = "Op"
        this.bOpShow = create_element("div",{className:"button", innerHTML:"show", onclick:function(e) {
            print("Reading operator");
            socket.send("phone,+COPS?");
        }});
        this.bOpShowAll = create_element("div",{className:"button", innerHTML:"showall", onclick:function(e) {
            print("Requesting operators...");
            socket.send("phone,+COPS=?");
        }});
        this.iOp = create_element("input",{type:"text", placeholder:"name", size:8});
        var iOp = this.iOp;
        this.bOpSet = create_element("div",{className:"button", innerHTML:"set", onclick:function(e) {
            let val = iOp.value;
            print("Setting operator to "+val);
            socket.send("phone,+COPS=1,0,\""+val+"\"");
        }});
        this.bOpAuto = create_element("div",{className:"button", innerHTML:"auto", onclick:function(e) {
            print("Auto-setting operator");
            socket.send("phone,+COPS=0");
        }});
        this.bOpDeauth = create_element("div",{className:"button", innerHTML:"deauth", onclick:function(e) {
            print("De-registering from operator");
            socket.send("phone,+COPS=2");
        }});
        this.bOpPreferred = create_element("div",{className:"button", innerHTML:"preferred", onclick:function(e) {
            print("Requesting preferred operators");
            socket.send("phone,+CPOL?");
        }});
        this.container= create_element("div", {className:"container hidden", id:"opContainer"});
        this.container.appendChild( createLabel("op:") );
        this.container.appendChild( this.bOpShow );
        this.container.appendChild( this.bOpShowAll );
        this.container.appendChild( iOp );
        this.container.appendChild( this.bOpSet );
        this.container.appendChild( this.bOpAuto );
        this.container.appendChild( this.bOpDeauth );
        this.container.appendChild( create_placeholder());
        this.container.appendChild( this.bOpPreferred );
    
    }
}