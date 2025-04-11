import { defineStore } from 'pinia';
import axios from 'axios';

if (process.env.IS_ELECTRON) {
    window.electron?.getBaseUrl().then(url => axios.defaults.baseURL = url);
} else {
    console.log("env BASE_URL", process.env.VUE_APP_BASE_URL);
    axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;
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