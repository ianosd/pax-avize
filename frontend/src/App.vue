<template>
  <RouterView />
</template>

<script>

import {mapState, mapActions} from 'pinia'
import { useOrderStore } from './components/orders'
import './assets/style.css'

export default {
  name: 'App',
  computed: {
    ...mapState(useOrderStore, ["orders"]),
  },
  methods: {
    ...mapActions(useOrderStore, ["loadReceipts"])
  },
  async beforeMount () {
    // TODO why does this fail
    console.log("This",this);
    this.loadReceipts();
  }
  }
</script>