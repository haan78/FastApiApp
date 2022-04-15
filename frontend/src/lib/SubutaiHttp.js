export default {
    default:{
        charset: "UTF-8",        
        method: "POST",
        jsonDataFormat:true,
        responseParser:null,
        data:null
    },
    activeRequestCount:0,

    onStart : function() {},
    onStop : function() {},

    isLoading() {
        return this.activeRequestCount > 0;
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

    queryTransform(obj) {
        var str = [];
        for (var p in obj) {
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        }            
        return str.join("&");
    },

    toISODateTimeFromat(d) {
        var tz = d.toString().split(" ").slice(-1)[0].trim().replace(/\(|\)|GMT/gm,'')
        var str = d.getFullYear()+
        "-"+(""+(d.getMonth()+1)).padStart(2,"0")+
        "-"+(""+d.getDate()).padStart(2,"0")+
        "T"+(""+d.getHours()).padStart(2,"0")+
        ":"+(""+d.getMinutes()).padStart(2,"0")+
        ":"+(""+d.getSeconds()).padStart(2,"0")+
        "."+(""+d.getMilliseconds()).padStart(3,"0")+
        tz;
        return str;
    },

    jsonTransform(data,level) {
        var l = ( level ? level : 0 );
        if ( data === null ) {
            return null;
        } else if ( typeof data === "object") { //object
            if (data instanceof Date) {
                return this.toISODateTimeFromat(data);
            } else if (Array.isArray( data )) {
                var arr = [];
                for(var i=0; i<data.length; i++) {
                    arr.push( this.jsonTransform(data[i]),l+1 );
                }
                return arr;
            } else {
                var obj = {};
                for( var k in data ) {
                    obj[k] = this.jsonTransform( data[k],l+1 );
                }
                return obj;
            }
        } else if (typeof data === "function") {
            return this.jsonTransform( data(l),l+1 );
        } else if (typeof data === "string" ) {
            var str = data.trim();
            if ( str === "" ) {
                return null;
            } else {
                return str;
            }
        } else {
            return data;
        }
    },
    __getDataCharacteristics(data,jsonDataFormat) {
        if ( typeof data === "function" ) {
            return this.__transform(data(),jsonDataFormat);
        } else if ( typeof data === "string" && data.trim() !== "" ) {
            return {
                "ContentType":"application/x-www-form-urlencoded",
                "method":"POST",
                "data":data.trim()
            };
        } else if ( data instanceof FormData ) {            
            return {
                "ContentType":"multipart/form-data",
                "method":"POST",
                "data":data
            };
        } else if ( typeof data === "object" && data !== null ) { //multipart/form-data
            if ( jsonDataFormat ) {
                return {
                    "ContentType":"application/json",
                    "method":"POST",
                    "data":JSON.stringify(this.jsonTransform(data))
                };
            } else {
                return {
                    "ContentType":"application/x-www-form-urlencoded",
                    "method":"POST",
                    "data":this.queryTransform(data)
                };                
            }           
        } else {
            return {
                "ContentType":"application/x-www-form-urlencoded",
                "method":"GET",
                "data":null
            };
        }
    },
    request(url,settings) {
        let self = this;
        let sett = ( settings !== null && typeof settings === "object" ) ? Object.assign(Object.create(self.default),settings) : Object.create(self.default);        
        return new Promise( (resolve,reject)=>{
            var HTTP = new XMLHttpRequest();
            HTTP.onreadystatechange = () =>{
                if (HTTP.readyState === 4) {
                    if (HTTP.status === 200) {
                        var response;
                        try {
                            if ( typeof sett.responseParser === "function" ) {
                                response = sett.responseParser(HTTP.responseText);
                            } else {
                                response = JSON.parse(HTTP.responseText);
                            }                            
                            resolve(response);
                        } catch (ex) {
                            ex.name = "ResponseParsError";
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

            self.up();
            var dc = self.__getDataCharacteristics(sett.data,sett.jsonDataFormat);

            HTTP.open(dc.method, url, true);
            HTTP.setRequestHeader("Content-type", dc.ContentType+";charset=" + sett.charset);            
            HTTP.send(dc.data);
        } );
    }
}