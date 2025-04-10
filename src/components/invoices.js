import { defineStore } from 'pinia';
import axios from 'axios';

if (process.env.IS_ELECTRON) {
    window.electron?.getBaseUrl().then(url => axios.defaults.baseURL = url);
} else {
    console.log("env BASE_URL", process.env.VUE_APP_BASE_URL);
    axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;
}

export const useInvoiceStore = defineStore('invoices',
    {
        state: () => {
            return { invoices: [] }
        },
        actions: {
            async loadReceipts() {
                var result = await axios.get(`/receipts`);
                console.log("HereA;");
                console.log(result);
                this.invoices = result.data;
            },
            async createInvoice(personArg) {
                var result = await axios.post('/receipts', { person: personArg });
                var receipt = result.data.receipt;
                this.invoices.push(receipt);
                console.log(`The invoices: ${this.invoices}`);
                console.log(receipt);
                return receipt;
            },
            async updateReceipt(receipt) {
                console.log("Doing it!");
                await axios.put("/receipts", receipt);
            },
            async getUniqueProductByCode(cod) {
                if (!cod) {
                    return null;
                }
                const response = await axios.get(`/products/${cod}`);
                const products = response.data;
                console.log("products", products);
                if (products.length != 1) {
                    return null;
                }
                return products[0];
            }
        }
    }
)