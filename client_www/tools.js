
SET_ATTRIBUTE = {
	"INPUT" : ["TYPE","SIZE","VALUE"],
	"TD":["COLSPAN"]
}

function create_element (type, props) {
	var ele = document.createElement(type);
    if (props != undefined) {

        for (var key in props) {
			if (props.hasOwnProperty(key)) {
				if (SET_ATTRIBUTE.hasOwnProperty(type) && key in SET_ATTRIBUTE[type]) {
					ele.setAttribute(key,props[key]);
				} else 
					ele[key] = props[key];
			}
		}
	}

	ele.removeClasses = function(array) {
		for (c in array) {
			if (ele.classList.contains(array[c])) {
				ele.classList.remove(array[c]);
			}
		}
	}

    return ele;
}

function get_children_with_props (parent,props) {
	var ret_array = [];
	var children = parent.childNodes;
	for (var c = 0; c < children.length; c++) {
		var element = children[c];
		var matching = true;
		
		for (var key in props) {
			if ( key == "class" && element.classList.contains(props[key]) ) {
				continue;
			}
			if ( element.getAttribute(key) == null || element.getAttribute(key) != props[key] ) {
				matching = false;
			}
		}
		if ( matching ) { ret_array.push(children[c]) }
	}
	return ret_array;
}


function create_placeholder(txt="") {
	return (txt == "") ? create_element("div",{className:"placeholder"}) : create_element("div",{className:"placeholderText", innerHTML:txt})
}


function download_page(container,url) {
	
	if (!container) container = create_element("div",{className:"preload"});
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function (e) { 
		if (xhr.readyState == 4 && xhr.status == 200) {
			container.innerHTML = xhr.responseText;
		}
	}
	xhr.open("GET", url, true);
	xhr.setRequestHeader('Content-type', 'text/html');
	xhr.send();
	return container;
}

HTMLElement.prototype.get_children_with_props = function (PROPS) { return get_children_with_props (this,PROPS) };
