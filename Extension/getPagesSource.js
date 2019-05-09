// @author Rob W <http://stackoverflow.com/users/938089/rob-w>
// Demo: var serialized_html = DOMtoString(document);


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

    return words;
	
}

chrome.runtime.sendMessage({
    action: "getSource",
    source: DOMtoString(document)
});