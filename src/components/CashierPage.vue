<template>
  <h1>Avize</h1>
  <!-- <div class="frame">
    <div v-for="(invoice, index) in invoices" :key="index" class="invoice-link" :class="stateClass(invoice.state)">
      <RouterLink 
              :to="{ name: 'invoice', params: {id:invoice.id} }"
            >
        <span style="color:black">#{{ invoice.number }}</span>
        <span>
          {{ stateText(invoice.state) }}
        </span>
        <span>{{ getInvoiceTotal(invoice) }} </span>
      </RouterLink>
    </div>
    </div>
  </div> -->
  <!-- TODO currency! -->

  <div class="folder-container">
    <div
      v-for="(invoice, index) in invoices"
      :key="invoice.id"
      class="folder-card"
      :class="stateClass(invoice.state)"
      draggable="true"
      @dragstart="dragStart($event, invoice)"
    >
      <div class="folder-header">
        <b>#{{ invoice.number }}</b>
        <span>{{ stateText(invoice.state) }}</span>
      </div>

      <div class="folder-contents">
        <div
          v-for="productEntry in invoice.products"
          :key="productEntry.productCode"
          class="folder-item"
        >
          {{ productEntry.productCode }} | {{ productEntry.quantity }} x
          {{ productEntry.price }}
        </div>
      </div>
      <button
        :disabled="invoice.state != 'submitted'"
        class="cashed-button"
        @click="
          invoices[index].state = 'cashed';
          updateReceipt(invoices[index]);
        "
      >
        Încasat
      </button>
    </div>
  </div>
</template>
<script>
import { useInvoiceStore } from "./invoices";
import { mapState, mapActions } from "pinia";

export default {
  computed: {
    ...mapState(useInvoiceStore, ["invoices"]),
  },
  methods: {
    dragStart(event, invoice) {
      const fileName = `aviz_${invoice.number}.xml`;
      const fileURL = `http://192.168.1.104:8082/receipts/${invoice.id}/saga`

      event.dataTransfer.setData(
        "DownloadURL",
        `text/xml:${fileName}:${fileURL}`
      );
    },
    ...mapActions(useInvoiceStore, ["loadReceipts", "updateReceipt"]),
    getInvoiceTotal(invoice) {
      const value = invoice.products
        .map((p) => p.price * p.quantity)
        .reduce((acc, a) => acc + a, 0);
      if (!isNaN(value)) {
        return `${value.toFixed(2)} RON`;
      } else {
        return "";
      }
    },
    stateClass(state) {
      return state;
    },
    stateText(state) {
      switch (state) {
        case "in_progress":
          return "în curs de editare";
        case "canceled":
          return "anulată";
        case "cashed":
          return "încasată";
        case "submitted":
          return "trimisă la caserie";
      }
      return "";
    },
  },
  beforeMount() {
    var self = this;
    const callback = () => {
      console.log("Self", self);
      self.loadReceipts();
    };
    this.interval = setInterval(callback, 2000);
  },
  unmounted() {
    clearInterval(this.interval);
  },
};
</script>