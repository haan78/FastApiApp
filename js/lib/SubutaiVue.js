import http from "./SubutaiHttp";
import cookie from "./SubutaiCookie";

export default {
    install: (app) => {
        // Plugin code goes here
        app.config.globalProperties.$subutai = {
            "cookie":cookie,
            "http":http
        };
    }
}