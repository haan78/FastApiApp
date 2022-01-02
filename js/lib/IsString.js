export default {
    anEmail:function(str){
        var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(str).toLowerCase());
    },
    aNumber:function(str) {
        var regx = /^[+-]?([1-9][0-9]*)(\.\d+)?$/;
        return regx.test(str);
    },

    aPhone :function(str) {
        var regx = /^[+]*[(]{0,1}[0-9]{1,3}[)]{0,1}[-\s./0-9]*$/g;
        return regx.test(str);
    },
    aTCKN:function(str) {
        if ( this.aNumber(str) && str.length == 11 ) {
            return true;
        } else {
            return false;
        }
    }

    
}