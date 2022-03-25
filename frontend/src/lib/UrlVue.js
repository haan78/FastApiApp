import Url from "./Url"
export default {
    install: (app) => {
        // Plugin code goes here
        app.config.globalProperties.$url = Url;
    }
}