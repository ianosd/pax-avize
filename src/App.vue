<template>
  <RouterView />
</template>

<script>

import {mapState, mapActions} from 'pinia'
import { useInvoiceStore } from './components/invoices'
import './assets/style.css'

export default {
  name: 'App',
  computed: {
    ...mapState(useInvoiceStore, ["invoices"]),
  },
  methods: {
    ...mapActions(useInvoiceStore, ["loadReceipts"])
  },
  async beforeMount () {
    // TODO why does this fail
    console.log("This",this);
    this.loadReceipts();
  }
  }
</script>