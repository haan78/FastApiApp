import IsString from "./IsString";
export default {
    install: (app) => {
        // Plugin code goes here
        app.config.globalProperties.$is = IsString;
    }
}