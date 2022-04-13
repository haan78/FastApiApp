
export default {
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
    toDateFromIso(isostr) {
        var ms = Date.parse(isostr);
        if ( !isNaN(ms) ) {
            return new Date(ms);
        } else {
            return null;
        }
    },
    toLocaleFromIso(isostr,type,locales, options) {
        var d  = this.toDateFromIso(isostr);
        if ( d !== null ) {
            if ( type == "date" ) {
                return d.toLocaleDateString(locales, options);
            } else if ( type == "time" ) {
                return d.toLocaleTimeString(locales, options);
            } else if (type == "datetime" ) {
                return d.toLocaleString(locales, options);
            } else {
                return "";
            }
        } else {
            return "";
        }
    },
    diffDays(date1, date2) {
        return Math.floor((Date.UTC(date2.getFullYear(), date2.getMonth(), date2.getDate()) - Date.UTC(date1.getFullYear(), date1.getMonth(), date1.getDate())) / (1000 * 60 * 60 * 24));
    }
}