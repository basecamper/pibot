class SysControls {

    constructor() {
        this.name = "Sys"
        this.container = create_element("div", {className:"container hidden", id:"sysContainer"});
        var logread = create_element("div",{className:"button", innerHTML:"phonelog", onclick:function() {
            socket.send("phonelog");
        }});
        this.container.appendChild( createLabel("Sys") );
        this.container.appendChild(logread);
    }
}
            