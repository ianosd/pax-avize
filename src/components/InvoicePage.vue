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
          <th>Validat</th>
        </tr>
        <tr v-for="(item, index) in invoice.products" :key="index">
          <td>
            <button @click="deleteProduct(index)" class="delete-button small-button" v-bind:disabled="!isEditableInvoice || invoice.products[index].valid">
              <FontAwesomeIcon :icon="faTrash" />
            </button>
          </td>
          <ProductView v-model:price="invoice.products[index].price"
            v-model:productCode="invoice.products[index].productCode"
            v-model:quantity="invoice.products[index].quantity" v-bind:valid="invoice.products[index].valid"
            @update:valid="
              (value) => {
                invoice.products[index].valid = value;
                updateReceipt(invoice);
              }
            " v-bind:editable="isEditableInvoice" />
        </tr>
      </table>
      <button style="margin-top: 10px" class="new-button" @click="newProduct" v-bind:disabled="!isEditableInvoice">
        <FontAwesomeIcon :icon="faPlus" />
        {{ $t('label.new_product') }}
      </button>
      <div style="
        width: 100%;
        margin-top: 20px;
        display: flex;
        justify-content: space-around;
      ">
        <button class="delete-button" @click="invoice.state = 'canceled'; updateReceipt(invoice);"
          v-bind:disabled="!isEditableInvoice"><FontAwesomeIcon :icon="faXmark"/> Anulează Aviz</button>
        <button class="submit-button" @click="invoice.state = 'submitted'; updateReceipt(invoice);"
          v-bind:disabled="!isEditableInvoice || !isValidInvoice"><FontAwesomeIcon :icon="faCashRegister"/> Trimite la caserie</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "pinia";
import { useInvoiceStore } from "./invoices";
import ProductView from "./ProductView.vue";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPlus, faTrash, faCashRegister, faXmark } from '@fortawesome/free-solid-svg-icons';

export default {
  components: {
    ProductView,
    FontAwesomeIcon
  },
  computed: {
    isValidInvoice() {
      return this.invoice.products.every(p => p.valid);
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
      faPlus, faTrash, faCashRegister, faXmark
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
      console.log(this.$props);
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
        price: "",
        valid: false,
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
