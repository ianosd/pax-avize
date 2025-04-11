<template>
  <h1>Avize</h1>
  <!-- <div class="frame">
    <div v-for="(order, index) in orders" :key="index" class="order-link" :class="stateClass(order.state)">
      <RouterLink 
              :to="{ name: 'order', params: {id:order.id} }"
            >
        <span style="color:black">#{{ order.number }}</span>
        <span>
          {{ stateText(order.state) }}
        </span>
        <span>{{ getOrderTotal(order) }} </span>
      </RouterLink>
    </div>
    </div>
  </div> -->
  <!-- TODO currency! -->

  <div class="folder-container">
    <div
      v-for="(order, index) in orders"
      :key="order.id"
      class="folder-card"
      :class="stateClass(order.state)"
      :draggable="order.state == 'submitted'"
      @dragstart="dragStart($event, order)"
    >
      <div class="folder-header">
        <b>#{{ order.number }}</b>
        <span>{{ stateText(order.state) }}</span>
      </div>

      <div class="folder-contents">
        <div
          v-for="productEntry in order.products"
          :key="productEntry.productCode"
          class="folder-item"
        >
          {{ productEntry.productCode }} | {{ productEntry.quantity }} x
          {{ productEntry.price }}
        </div>
      </div>
      <button
        :disabled="order.state != 'submitted'"
        class="cashed-button"
        @click="
          orders[index].state = 'cashed';
          updateOrder(orders[index]);
        "
      >
        Încasat
      </button>
    </div>
  </div>
</template>
<script>
import { useOrderStore } from "./orders";
import { mapState, mapActions } from "pinia";

export default {
  computed: {
    ...mapState(useOrderStore, ["orders"]),
    baseURL() {
      return this.electronURL ? this.electronURL : process.env.VUE_APP_BASE_URL;
    }
  },
  data() {
    return {
      electronURL: ""
    }
  },
  methods: {
    dragStart(event, order) {
      console.log("Yuhu!")
      // TODO fix this
      const fileURL = `${this.baseURL}/receipts/${order.id}/saga`
      if (window.electron) {
        event.preventDefault();
        window.electron?.startDrag(fileURL);
      } else {
        console.log("Setting data", fileURL);
        event.dataTransfer.setData(
          "DownloadURL",
          `text/plain:aviz_${order.number}.txt:${fileURL}`
        );}
    },
    ...mapActions(useOrderStore, ["loadReceipts", "updateOrder"]),
    getOrderTotal(order) {
      const value = order.products
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

    window.electron?.getBaseUrl().then(url => this.electronURL=url);
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