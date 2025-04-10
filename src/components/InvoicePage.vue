<template>
  <div class="container">
    <nav style="width: 100%; display: flex; justify-content:space-around">
      <button @click="$router.push('/operator')">Lista avize</button>
      <button @click="onNewInvoice">Aviz nou</button>
    </nav>
    <div class="centered" v-if="invoiceLoaded">
      <h1>{{ $t('label.aviz') }} #{{ invoice.number }}</h1>
      <i style="margin-bottom: 10px;">{{ invoiceStateText }}</i>
      <table>
        <tr>
          <th></th>
          <th>Cod</th>
          <th>Cant.</th>
          <th>Preț</th>
          <th>P. Saga </th>
        </tr>
          <ProductView v-for="(item, index) in invoice.products" :key="index" 
          v-model:price="invoice.products[index].price"
            v-model:productCode="invoice.products[index].productCode"
            v-model:quantity="invoice.products[index].quantity"
            v-bind:editable="isEditableInvoice"
            @deleteItem="deleteProduct(index)" />
      </table>
      <button style="margin-top: 10px" class="new-button" @click="newProduct" v-bind:disabled="!isEditableInvoice">
        <FontAwesomeIcon :icon="faPlus" />
        {{ $t('label.new_product') }}
      </button>
      <span style="margin-top: 10px;">Total: <b>{{ total }}</b></span>
      <div style="
        width: 100%;
        margin-top: 20px;
        display: flex;
        justify-content: space-around;
      ">
        <button v-if="isModifyable" class="delete-button" @click="invoice.state = 'canceled'; updateReceipt(invoice);"
          v-bind:disabled="!isEditableInvoice"><FontAwesomeIcon :icon="faXmark"/> Anulează Aviz</button>
        <button v-if="isModifyable" class="submit-button" @click="invoice.state = 'submitted'; updateReceipt(invoice);"
          v-bind:disabled="!isValidInvoice"><FontAwesomeIcon :icon="faCashRegister"/> Trimite la caserie</button>
        <button v-if="!isModifyable" class="edit-button" @click="invoice.state = 'in_progress'; updateReceipt(invoice);"
          ><FontAwesomeIcon :icon="faEdit"/>Modifică</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "pinia";
import { useInvoiceStore } from "./invoices";
import ProductView from "./ProductView.vue";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPlus, faTrash, faCashRegister, faXmark, faEdit } from '@fortawesome/free-solid-svg-icons';

export default {
  components: {
    ProductView,
    FontAwesomeIcon
  },
  computed: {
    isModifyable() {
      console.log("Invoice", this.invoice.state);
      return !['submitted', 'canceled'].includes(this.invoice.state);
    },
    total () {
      return this.invoice.products.map(p => p.quantity*p.price).reduce((s, v) => s+v, 0);
    },
    isValidInvoice() {
      function isValid(p) {
        return p.productCode != "" && p.quantity != "" && p.price != "";
      }

      return this.invoice.products.length > 0 && this.invoice.products.every(isValid);
    },
    isEditableInvoice() {
      return this.invoice.state == "in_progress";
    },
    invoiceStateText() {
      switch (this.invoice.state) {
        case "in_progress":
          return "în curs de editare";
        case "canceled":
          return "anulat";
        case "submitted":
          return "trimis la caserie";
        case "cashed":
          return "încasat";
      }
      return "";
    },
    ...mapState(useInvoiceStore, ["invoices"]),
  },
  props: {
    id: Number,
  },
  data() {
    return {
      productCode: "",
      quantity: 1,
      invoiceLoaded: false,
      invoice: {},
      faPlus, faTrash, faCashRegister, faXmark, faEdit
    };
  },
  watch: {
    invoices: {
      handler(newInvoices) {
        this.updateInvoice(newInvoices, this.id);
      },
      deep: true, // Ensures Vue watches changes inside the array
      immediate: true, // Runs the handler immediately on component mount
    },
    id: {
      handler(to) {
        console.log(to);
        this.updateInvoice(this.invoices, this.id);
      },
    },
  },
  methods: {
    onNewInvoice() {
      this.createInvoice("cristi").then(invoice => {
        this.$router.push({ name: "invoice", params: { id: invoice.id } });
      });
    },
    ...mapActions(useInvoiceStore, ["createInvoice", "loadReceipts"]),
    updateInvoice(invoices, id) {
      const index = invoices.findIndex(
        (invoice) => invoice.id == id
      );
      this.invoice = invoices[index];
      this.invoiceLoaded = this.invoice !== undefined;
    },
    ...mapActions(useInvoiceStore, ["updateReceipt"]),
    newProduct() {
      this.invoice.products.push({
        productCode: "",
        quantity: "",
        price: ""
      });
      this.updateReceipt(this.invoice);
    },
    deleteProduct(index) {
      this.invoice.products.splice(index, 1);
      this.updateReceipt(this.invoice);
    },
  },
  beforeMount() {
    this.updateInvoice(this.invoices, this.id);
  },
};
</script>
