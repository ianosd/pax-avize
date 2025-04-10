<template>
  <div class="container">
  <nav style="width: 100%; display: flex; justify-content:space-around">
    <button @click="$router.push('/operator')">Lista avize</button>
    <button @click="onNewOrder">Aviz nou</button>
  </nav>
  <div class="centered">
  <h1>{{ $t('label.avize') }}</h1>
  <div class="frame">
    <div v-for="(Order, index) in Orders" :key="index" class="Order-link" :class="stateClass(Order.state)">
      <RouterLink 
              :to="{ name: 'Order', params: {id:Order.id} }"
            >
        <span style="color:black">#{{ Order.number }}</span>
        <span>
          {{ stateText(Order.state) }}
        </span>
        <!-- TODO currency! -->
        <span>{{ getOrderTotal(Order) }} </span>
      </RouterLink>
    </div>
    </div>
  </div>
</div>
</template>

<script>
import { useOrderStore } from './Orders'
import { mapState, mapActions } from 'pinia';
export default {
  computed: {
    ...mapState(useOrderStore, ["Orders"]),
  },
  methods: {
    onNewOrder() {
      this.createOrder("cristi").then(Order=> {
        this.$router.push({name:"Order", params:{id:Order.id}});
      });
    },
    ...mapActions(useOrderStore, ["createOrder", "loadReceipts"]),
    getOrderTotal(Order) {
      const value = Order.products.map(p => p.price*p.quantity).reduce((acc, a) => acc + a, 0);
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
/* Add styling for the Order page */
</style>
