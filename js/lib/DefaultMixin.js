
export default {
    
    methods:{
        link(path) {            
            if (this.$router) {
                if (this.$router.currentRoute.path != path ) {
                    this.$router.push(path);
                }
            }            
        }
    }
}