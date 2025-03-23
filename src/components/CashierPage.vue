<template>
  <div class="centered">
    <h1>Avize</h1>
  <div class="frame">
    <div v-for="(invoice, index) in invoices" :key="index" class="invoice-link" :class="stateClass(invoice.state)">
      <RouterLink 
              :to="{ name: 'invoice', params: {id:invoice.id} }"
            >
        <span style="color:black">#{{ invoice.number }}</span>
        <span>
          {{ stateText(invoice.state) }}
        </span>
        <!-- TODO currency! -->
        <span>{{ getInvoiceTotal(invoice) }} </span>
      </RouterLink>
    </div>
    </div>
  </div>
</template>
<script>
import { useInvoiceStore } from './invoices'
import { mapState, mapActions } from 'pinia';

export default {
  computed: {
    ...mapState(useInvoiceStore, ["invoices"]),
  },
  methods: {
    ...mapActions(useInvoiceStore, ["loadReceipts"]),
    getInvoiceTotal(invoice) {
      const value = invoice.products.map(p => p.price*p.quantity).reduce((acc, a) => acc + a, 0);
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
          return "trimisă la caserie"
      }
      return "";
    }
  },
  beforeMount() {
    var self = this;
    const callback = () => {
        console.log("Self", self);
        self.loadReceipts();
    }
    this.interval = setInterval(callback, 2000);
  },
  unmounted() {
    clearInterval(this.interval);
  }
};
</script>