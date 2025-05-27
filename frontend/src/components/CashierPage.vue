<template>
  <div>
  <h1>Editare aviz <button @click="resetOrder()">Aviz nou</button></h1>
  <OrderPage ref="orderPage" :id="orderPageId" :isCashierMode="true"/>
  </div>
  <hr/>
  <h1>Avize</h1>
  <hr />
  <!-- TODO currency! -->

  <div class="folder-container">
    <div
      v-for="order in displayedOrders"
      :key="order.id"
      class="folder-card"
      :class="stateClass(order.state)"
      :draggable="order.state == 'submitted'"
      @dragstart="dragStart($event, order)"
    >
      <div class="folder-header">
        <span><b>#{{ order.number }}</b> {{ stateText(order.state) }}</span>
        <button @click="orderPageId=order.id">Editează</button>
      </div>

      <div class="folder-contents">
        <table>
          <thead>
            <tr>
              <th>Produs</th>
              <th>Cant.</th>
              <th>Preț</th>
              <th>Val.</th>
            </tr>
          </thead>
          <tbody>
            <ReadOnlyProductView
              v-for="(product, index) in order.products"
              :key="index"
              :productCode="product.productCode"
              :quantity="product.quantity"
              :price="product.price"
            />
          </tbody>
        </table>
      </div>
      <span style="text-align: right; margin-top: 10px">
        <b>Total: {{ getOrderTotal(order) }} </b>
      </span>
      <button
        :disabled="order.state != 'submitted'"
        class="cashed-button"
        @click="
          order.state = 'cashed';
          updateOrder(order);
        "
      >
        Marchează ca încasat
      </button>
    </div>
  </div>
</template>
<script>
import { useOrderStore } from "./orders";
import { mapState, mapActions } from "pinia";
import ReadOnlyProductView from "./ReadOnlyProductView.vue";
import OrderPage from "./OrderPage.vue";

export default {
  components: {
    ReadOnlyProductView,
    OrderPage
  },
  computed: {
    ...mapState(useOrderStore, ["orders"]),
    baseURL() {
      return this.electronURL ? this.electronURL : process.env.VUE_APP_BASE_URL;
    },
    displayedOrders() {
      return (
        this.orders
          .sort((a, b) => b.number - a.number)
      );
    },
  },
  data() {
    return {
      electronURL: "",
      orderPageId: null
    };
  },
  methods: {
    resetOrder() {
      this.orderPageId = null;
      this.$refs.orderPage.resetOrder();
    },
    dragStart(event, order) {
      const fileURL = `${this.baseURL}/receipts/${order.id}/saga`;
      if (window.electron) {
        event.preventDefault();
        window.electron?.startDrag(fileURL);
      } else {
        console.log("Setting data", fileURL);
        event.dataTransfer.setData(
          "DownloadURL",
          `text/plain:aviz_${order.number}.txt:${fileURL}`
        );
      }
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
          return "anulat";
        case "cashed":
          return "încasat";
        case "submitted":
          return "trimis la caserie";
      }
      return "";
    },
  },
  beforeMount() {
    var self = this;

    window.electron?.getBaseUrl().then((url) => (this.electronURL = url));
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