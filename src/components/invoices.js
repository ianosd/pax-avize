import { defineStore } from 'pinia';
import axios from 'axios';
axios.defaults.baseURL = 'http://localhost:8082';

export const useInvoiceStore = defineStore('invoices', 
    {
        state: () => {
            return {invoices: []}
        },
        actions: {
            async loadReceipts() {
                var result = await axios.get('/receipts');
                console.log("HereA;");
                console.log(result);
                this.invoices = result.data;
            },
            async createInvoice(personArg) {
                var result = await axios.post('/receipts', {person: personArg});
                var receipt = result.data.receipt;
                this.invoices.push(receipt);
                console.log(`The invoices: ${this.invoices}`);
                console.log(receipt);
                return receipt;
            },
            async updateReceipt(receipt) {
                console.log("Doing it!");
                await axios.put("/receipts", receipt);
            }
        }
    }
)