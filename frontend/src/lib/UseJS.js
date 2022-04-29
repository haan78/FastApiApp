export default (options)=> {

    var defaults = Object.assign({
        end:() => { console.log("end"); },
        jslist:[],
        csslist:[],
        hash:"rnd" + (new Date()).getTime()
    },( options!==null && typeof options === "object" ? options :{}));    

    return {
        jslist: defaults.jslist,
        csslist: defaults.csslist, 
        hash: defaults.hash,       
        __onEnd: defaults.end,
        js: function (src, options) {
            var type = (options &&  options.type) ?  options.type : "text/javascript";
            var before = (options &&  options.before) ?  options.before : ()=>{};
            this.jslist.push({ "src": src, "type": type, "before":before });
            return this;
        },
        css: function (src) {
            this.csslist.push({ "src": src });
            return this;
        },
        _nextJs: function (ind,callback) {
            let self = this;

            if ( ind < self.jslist.length ) {
                var script = document.createElement('script');
                script.setAttribute("type", self.jslist[ind].type);
                script.setAttribute("src", self.jslist[ind].src + (self.hash ? "?"+self.hash : "" ));
                script.onerror = function () {
                    throw new Error("Dynamic script loading error (" + this.src + ")");
                };
                script.onload = function () {
                    self._nextJs(ind+1,callback);
                };                
                document.getElementsByTagName("head")[0].appendChild(script);
                self.jslist[ind].before(script);
            } else {
                callback();
            }
        },
        load: function () {
            let self = this;
            window.addEventListener("load",function() {                
                for (var i = 0; i < self.csslist.length; i++) {
                    var link = document.createElement("link");
                    link.setAttribute("rel", "stylesheet");
                    link.setAttribute("type", "text/css");
                    link.setAttribute("href", self.csslist[i].src + (self.hash ? "?"+self.hash : "" ));
                    document.getElementsByTagName("head")[0].appendChild(link);
                }
    
                self._nextJs(0,self.__onEnd);
            });
        }
    };
};
