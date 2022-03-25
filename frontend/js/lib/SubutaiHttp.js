export default {
    default:{
        charset: "UTF-8",
        useDataTransform:true
    },
    activeRequestCount:0,

    onStart : function() {},
    onStop : function() {},

    isLoading() {
        return this.activeRequestCount > 0;
    },

    isAppError(response) {
        if ( typeof response === "object" && response === null &&  response.ERROR ) {
            var err;
            if ( typeof response.ERROR.message  === "string") {
                err = new Error(response.ERROR.message);
            } else {
                return "ERROR object exists but message can`t read";
            }
        }
        return false;
    },

    validate(response) {
        if ( typeof response === "object" && typeof response.success === "boolean" && typeof response.data !== "undefined" ) {
            return true;
        } else {
            return false;
        }
    },

    up() {       
        if (this.activeRequestCount === 0) {
            if (  typeof this.onStart ===  "function") {
                this.onStart();
            }
        } 
        this.activeRequestCount += 1;       
    },

    down() {
        if ( this.activeRequestCount > 0 ) {
            this.activeRequestCount -= 1;       
        } 
        if ( this.activeRequestCount === 0 ) {
            if (  typeof this.onStop ===  "function") {
                this.onStop();
            }
        }
    },

    dataTransform(data,level) {
        var l = ( level ? level : 0 );
        if ( data === null ) {
            return null;
        } else if ( typeof data === "object") { //object
            if (Array.isArray( data )) {
                var arr = [];
                for(var i=0; i<data.length; i++) {
                    arr.push( this.dataTransform(data[i]),l+1 );
                }
                return arr;
            } else {
                var obj = {};
                for( var k in data ) {
                    obj[k] = this.dataTransform( data[k],l+1 );
                }
                return obj;
            }
        } else if (typeof data === "function") {
            return this.dataTransform( data(l),l+1 );
        } else if (typeof data === "string" ) {
            var str = data.trim();
            if ( str === "" ) {
                return null;
            } else {
                return str;
            }
        } else if (data instanceof Date) {
            return data.toISOString();
        } else {
            return data;
        }
    },
    request(url,data,settings) {
        let self = this;

        let sett = self.default;
        if ( typeof settings === "object" && settings!==null ) {
            for(var k in self.default) {
                if ( typeof settings[k] !== "undefined" ) {
                    sett[k] = settings[k];
                }
            }
        }
        return new Promise( (resolve,reject)=>{
            var HTTP = new XMLHttpRequest();
            HTTP.onreadystatechange = () =>{
                if (HTTP.readyState === 4) {
                    if (HTTP.status === 200) {
                        var response;
                        try {
                            response = JSON.parse(HTTP.responseText);
                            resolve(response);
                        } catch (ex) {
                            ex.name = "JSONParsError";
                            reject(ex,HTTP.responseText);
                            return;
                        }
                    } else {
                        var err = new Error();
                        err.statusText = HTTP.statusText;
                        try {
                            err.json = JSON.parse(HTTP.responseText);                            
                            if ( err.json.detail ) {
                                err.message = err.json.detail.toString();
                                err.name = "ServerDetailedError"
                                reject( err);
                            } else {
                                err.message = "Unknown Error Message"
                                err.name = "ServerUnknownError"
                                reject(err);
                            }
                        } catch {                            
                            err.message = HTTP.responseText;
                            err.name = "ServerRawError";                        
                            err.json = null;
                            reject(err);
                        }
                    }
                    self.down();
                }
            }

            HTTP.open("POST", url, true);
            HTTP.setRequestHeader("Content-type", "application/json;charset=" + sett.charset);
            var d; 
            if (sett.useDataTransform) {
                d = self.dataTransform(data);
            } else {
                d = data;
            }
            self.up();
            HTTP.send(JSON.stringify(d));
        } );
    }
}