export default {
    COOKIE_NAME:"SUBUTAI",
    COOKIE_DATA : false,

    get(options) {
        var op = {
            "removeAfterRead":false,
            "refresh":false
        };

        if ( typeof options === "object" && options !== null ) {
            Object.keys(op).forEach((key)=>{
                if ( typeof options[key] !== "undefined" ) {
                    op[key] = options[key];
                }
            });
        }        
        
        if ( op.refresh || this.COOKIE_DATA === false ) {
            this.COOKIE_DATA = this.__cookie(op.removeAfterRead);
        }
        return this.COOKIE_DATA;
    },
    __remove() {
        window.document.cookie = encodeURIComponent(this.COOKIE_NAME) + "=; Max-Age=0;";
    },
    __cookie(remove) {
        const value = "; " + window.document.cookie;
        const parts = value.split("; " + this.COOKIE_NAME + "=");
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