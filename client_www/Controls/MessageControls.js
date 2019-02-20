class MessageControls {

    constructor() {
        this.name = "Msg"
        this.container = create_element("div", {id:"msgContainer"});
        
        var clear = create_element("div",{className:"button", innerHTML:"clear", onclick:function() {
            messages.innerHTML = "";
        }});
        
        this.container.appendChild(clear);
    }
}
            