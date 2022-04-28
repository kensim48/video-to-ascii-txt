import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import { VueReCaptcha } from "vue-recaptcha-v3";

Vue.config.productionTip = false;
Vue.use(VueReCaptcha, { siteKey: "6LeQJ6gfAAAAAItnrDXbQyP8WanvmxuzSS3BnND8" });

new Vue({
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
