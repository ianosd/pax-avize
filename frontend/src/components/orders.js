import { defineStore } from 'pinia';
import axios from 'axios';

// Set the api url for order data
if (process.env.IS_ELECTRON) {
    window.electron?.getBaseUrl().then(url => axios.defaults.baseURL = url);
} else {
    if (process.env.VUE_APP_BASE_URL == "origin_slash_api") {
        axios.defaults.baseURL = `${window.location.origin}/api`;
    } else {
        axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;
    }
    console.log("backend URL", axios.defaults.baseURL);
}

export const useOrderStore = defineStore('order',
    {
        state: () => {
            return { orders: [] }
        },
        actions: {
            async loadReceipts() {
                var result = await axios.get(`/receipts`);
                this.orders = result.data;
            },
            async createOrder(personArg) {
                var result = await axios.post('/receipts', { person: personArg });
                var receipt = result.data.receipt;
                this.orders.push(receipt);
                return receipt;
            },
            async updateOrder(receipt) {
                await axios.put("/receipts", receipt);
            },
            async getUniqueProductByCode(cod) {
                if (!cod) {
                    return null;
                }
                const response = await axios.get(`/products/${cod}`);
                const products = response.data;
                if (products.length != 1) {
                    return null;
                }
                return products[0];
            }
        }
    }
)