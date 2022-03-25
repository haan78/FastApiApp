import Memo from "./Memo";
export default {
    install: (app) => {
        // Plugin code goes here
        app.config.globalProperties.$memo = Memo;
    }
}