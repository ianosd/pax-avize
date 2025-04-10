import { createApp } from 'vue'
import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import { createPinia } from 'pinia';
import { createI18n } from 'vue-i18n';

import App from './App.vue'
import OrderPage from './components/OrderPage.vue';
import HomePage from './components/HomePage.vue';
import CashierPage from './components/CashierPage.vue';

const router = createRouter({
    history: process.env.IS_ELECTRON ? createWebHashHistory() : createWebHistory(),
    routes:[
        { path: '/', component: CashierPage },
        { path: '/order/:id', component: OrderPage, name: "order", props: true },
        {path: '/operator', component: HomePage}
    ]
})

const i18n = createI18n({
  locale: 'ro',
  fallbackLocale: 'ro',
  messages: {
    ro: {
      label: {
        aviz: 'Aviz',
        delete: "Șterge",
        new_product: "Adaugă produs",
        avize: 'Avize'
      }
    }
  }
})

const app = createApp(App);
app.use(i18n);
app.use(router);
const pinia = createPinia()
app.use(pinia);


app.mount('#app')
