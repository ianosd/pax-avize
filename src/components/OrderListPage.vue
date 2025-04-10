<template>
  <div class="container">
  <nav style="width: 100%; display: flex; justify-content:space-around">
    <button @click="$router.push('/operator')">Lista avize</button>
    <button @click="onNewOrder">Aviz nou</button>
  </nav>
  <div class="centered">
  <h1>{{ $t('label.avize') }}</h1>
  <div class="frame">
    <div v-for="(order, index) in orders" :key="index" class="order-link" :class="stateClass(order.state)">
      <RouterLink 
              :to="{ name: 'order', params: {id:order.id} }"
            >
        <span style="color:black">#{{ order.number }}</span>
        <span>
          {{ stateText(order.state) }}
        </span>
        <!-- TODO currency! -->
        <span>{{ getOrderTotal(order) }} </span>
      </RouterLink>
    </div>
    </div>
  </div>
</div>
</template>

<script>
import { useOrderStore } from './orders'
import { mapState, mapActions } from 'pinia';
export default {
  computed: {
    ...mapState(useOrderStore, ["orders"]),
  },
  methods: {
    onNewOrder() {
      this.createOrder("cristi").then(order=> {
        this.$router.push({name:"order", params:{id:order.id}});
      });
    },
    ...mapActions(useOrderStore, ["createOrder", "loadReceipts"]),
    getOrderTotal(order) {
      const value = order.products.map(p => p.price*p.quantity).reduce((acc, a) => acc + a, 0);
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
