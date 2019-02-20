

class VoiceMailControls {
    constructor() {
        this.name = "Voice Mail"
        this.iNum = create_element("input",{type:"text", placeholder:"number", size:20});
        var iNum = this.iNum;
        this.iName = create_element("input",{type:"text", placeholder:"name", size:20});
        var iName = this.iName;
        
        this.bNumSet = create_element("div",{className:"button", innerHTML:"set", onclick:function(e) {
            let num = iNum.value;
            let name = iName.value;
            print("Setting voice mail number to "+num+", "+name);
            socket.send("phone,+CCVM=\""+num+"\",\""+name+"\"");
        }});
        
        this.container= create_element("div", {className:"container hidden", id:"opContainer"});
        this.container.appendChild( createLabel("voice mail:") );
        this.container.appendChild( iNum );
        this.container.appendChild( iName );
        this.container.appendChild( this.bNumSet );
    
    }
}