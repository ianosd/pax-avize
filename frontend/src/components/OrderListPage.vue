<template>
  <div class="container">
  <OperatorNav></OperatorNav>
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
import OperatorNav from './OperatorNav.vue';
import { useOrderStore } from './orders'
import { mapState, mapActions } from 'pinia';
export default {
  components: {
    OperatorNav
  },
  computed: {
    ...mapState(useOrderStore, ["orders"]),
  },
  methods: {
    ...mapActions(useOrderStore, ["loadReceipts"]),
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
          return "anulat";
        case "cashed":
          return "încasat";
        case "submitted":
          return "trimis la caserie"
      }
      return "";
    }
  }
};
</script>

<style scoped>
/* Add styling for the Order page */
</style>
