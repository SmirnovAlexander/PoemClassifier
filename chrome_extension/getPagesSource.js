function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}
function DOMtoString(document_root) {
    var html = '',
        node = document_root.firstChild;
    while (node) {
        switch (node.nodeType) {
        case Node.ELEMENT_NODE:
            html += node.outerHTML;
            break;
        case Node.TEXT_NODE:
            html += node.nodeValue;
            break;
        case Node.CDATA_SECTION_NODE:
            html += '<![CDATA[' + node.nodeValue + ']]>';
            break;
        case Node.COMMENT_NODE:
            html += '<!--' + node.nodeValue + '-->';
            break;
        case Node.DOCUMENT_TYPE_NODE:
            // (X)HTML documents are identified by public identifiers
            html += "<!DOCTYPE " + node.name + (node.publicId ? ' PUBLIC "' + node.publicId + '"' : '') + (!node.publicId && node.systemId ? ' SYSTEM' : '') + (node.systemId ? ' "' + node.systemId + '"' : '') + '>\n';
            break;
        }
        node = node.nextSibling;
    }
	
    // Getting string containing russian words
	var words = "";
	var russianLetters = "ёйцукенгшщзхъфывапролджэячсмитьбю ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЧСМИТЬБЮ";
	for (var i = 0; i < html.length; i++) {
		for (var j = 0; j < russianLetters.length; j++){
			if (html.charAt(i) == russianLetters.charAt(j)){words = words + html.charAt(i)};
		}    
    }
    words = words.toLowerCase();
    words = words.replace(/\s+/g,' ').trim();
    
	// Making a post request with our words
	var x = new XMLHttpRequest();
    x.open("POST", "http://localhost:9090");
    x.send(words);

	wait(500);
		
	// Making a get request for the result
	var y = new XMLHttpRequest();   
    y.open('GET', 'http://localhost:9090', false);
    y.send();

	// Handling errors
    if (y.status != 200) {
       words = y.status + ': ' + y.statusText;
    } else {
       words = y.responseText;
    }   
	
    return words;
	
}

chrome.runtime.sendMessage({
    action: "getSource",
    source: DOMtoString(document)
});