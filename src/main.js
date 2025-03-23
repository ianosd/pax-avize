import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia';

import App from './App.vue'
import InvoicePage from './components/InvoicePage.vue';
import HomePage from './components/HomePage.vue';
import CashierPage from './components/CashierPage.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: HomePage },
        { path: '/invoice/:id', component: InvoicePage, name: "invoice", props: true },
        {path: '/cashier', component: CashierPage}
    ]
})

const app = createApp(App);
app.use(router);
const pinia = createPinia()
app.use(pinia);


app.mount('#app')
