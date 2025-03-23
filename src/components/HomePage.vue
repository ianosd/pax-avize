<template>
  <div class="container">
  <nav style="width: 100%; display: flex; justify-content:space-around">
    <button @click="$router.push('/')">Lista avize</button>
    <button @click="onNewInvoice">Aviz nou</button>
  </nav>
  <div class="centered">
  <h1>Invoices</h1>
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
    onNewInvoice() {
      this.createInvoice("cristi").then(invoice=> {
        this.$router.push({name:"invoice", params:{id:invoice.id}});
      });
    },
    ...mapActions(useInvoiceStore, ["createInvoice", "loadReceipts"]),
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
  

  }
};
</script>

<style scoped>
/* Add styling for the invoice page */
</style>
