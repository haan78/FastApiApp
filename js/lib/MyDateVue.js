import MyDate from "./MyDate"
export default {
    install: (app) => {
        // Plugin code goes here
        app.config.globalProperties.$date = MyDate;
    }
}