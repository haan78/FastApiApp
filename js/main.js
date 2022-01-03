import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import locale from 'element-plus/lib/locale/lang/tr';
import subutai from './lib/SubutaiVue';

import comp from './Main.vue';

let app = document.getElementById("app");
app.innerHTML = "";
createApp(comp).use(ElementPlus, { locale }).use(subutai).mount(app);
//createApp(comp).use(subutai).mount(app);
console.log(window.document.cookie);
console.log(typeof window.document.cookie);