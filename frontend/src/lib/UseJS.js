export default ()=> {
    var rnd = "?rnd" + (new Date()).getTime();

    return {
        jslist: [],
        csslist: [],
        onBeforeStart() {},
        js: function (src, options) {
            var type = (options &&  options.type) ?  options.type : "text/javascript";
            var before = (options &&  options.before) ?  options.before : ()=>{};
            this.jslist.push({ "src": src, "type": type, "before":before });
            return this;
        },
        css: function (src,options) {
            var type = (options &&  options.type) ?  options.type : "text/css";
            var before = (options &&  options.before) ?  options.before : ()=>{};
            this.csslist.push({ "src": src, "type": type, "before":before });
            return this;
        },
        _nextJs: function (ind) {
            let self = this;
            if ( ind < self.jslist.length ) {
                var script = document.createElement('script');
                script.setAttribute("type", self.jslist[ind].type);
                script.setAttribute("src", self.jslist[ind].src + rnd);
                script.onerror = function () {
                    throw new Error("Dynamic script loading error (" + this.src + ")");
                };
                script.onload = function () {
                    self._nextJs(ind+1);
                };
                self.jslist[ind].before(script);
                document.getElementsByTagName("head")[0].appendChild(script);
            }
        },
        load: function () {
            let self = this;
            window.addEventListener("load",function() {
                self.onBeforeStart();
                for (var i = 0; i < self.csslist.length; i++) {
                    var link = document.createElement("link");
                    link.setAttribute("rel", "stylesheet");
                    link.setAttribute("type", self.csslist[i].type);
                    link.setAttribute("href", self.csslist[i].src + rnd);
                    self.csslist[i].before(link);
                    document.getElementsByTagName("head")[0].appendChild(link);
                }
    
                if (self.jslist.length > 0) {
                    self._nextJs(0);
                }
            });
        }
    };
};
