export default {    

    get(name,options) {
        var op = {
            "removeAfterRead":false,
            "refresh":false,
            "json64":false
        };

        if ( typeof options === "object" && options !== null ) {
            Object.keys(op).forEach((key)=>{
                if ( typeof options[key] !== "undefined" ) {
                    op[key] = options[key];
                }
            });
        }
        
        var value = this.__cookie(name,op.removeAfterRead);
        if ( op.json64 ) {            
            return this.__b64DecodeUnicode(value);
        } else {
            return value;
        }
    },

    __b64DecodeUnicode(str) {
        return decodeURIComponent(atob(str).replace(/(.)/g, function (m, p) {
            var code = p.charCodeAt(0).toString(16).toUpperCase();
            if (code.length < 2) {
                code = '0' + code;
            }
            return '%' + code;
        }));
    },

    __remove(name) {
        window.document.cookie = encodeURIComponent(name) + "=; Max-Age=0;";
    },

    __cookie(name,remove) {
        const value = "; " + window.document.cookie;
        const parts = value.split("; " + name + "=");
        //console.log(parts);
        if (parts.length == 2) {
            const vlu = parts.pop().split(";").shift();
            const decode_vlu = decodeURIComponent(vlu);
            const replace_vlu = decode_vlu.replace(/[+]/g, ' ');
            if ( remove ) {
                this.__remove();
            }
            var result = false;
            try {
                result = JSON.parse(replace_vlu);
            } catch {
                result = replace_vlu;
            }            
            return result;
        } else {
            return false;
        }
    },
}