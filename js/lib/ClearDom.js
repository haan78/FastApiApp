export default (options) => {
    var defaults = {
        "margin":"0",
        "padding":"0",
        "tag":"div"
    };

    if ( typeof options === "object" && options !== null ) {
        for(var k in defaults) {
            if ( typeof options[k] !== "undefined") {
                defaults[k] = options[k];
            }
        }
    }

    window.document.body.innerHTML = "";
    window.document.body.style.margin = defaults.margin;
    window.document.body.style.padding = defaults.padding;
    var container = document.createElement(defaults.tag);
    document.body.appendChild( container );

    return container;
}