export default {
    get(str) {
        return str
            .replaceAll(/'/g,'&#39;')
            .replaceAll(/"/g,"&#34;")
            .replaceAll(/\\/g,"&#92;")
            .replaceAll(/\//g,'&#47;')
            .replaceAll(/>/g,'&#62;')
            .replaceAll(/</g,'&#60;')
            .replaceAll(/\n/g,"<br/>")
            .replaceAll(/\r/g,""); 
    },
    set(str) {
        return str
            .replaceAll("<br/>","\n")            
            .replaceAll("&#60;",'<')
            .replaceAll("&#62;",'>')
            .replaceAll("&#47;",'/')
            .replaceAll("&#92;","\\")
            .replaceAll("&#34;","\"")
            .replaceAll("&#39;",'\'');
    }
}