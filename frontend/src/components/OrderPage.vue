<template>
  <div class="container">
    <OperatorNav v-if="!isCashierMode"></OperatorNav>
    <div class="centered" v-if="orderLoaded">
      <h1 v-if="id!=null">{{ $t("label.aviz") }} #{{ order.number }}</h1>
      <h1 v-else>Aviz nou</h1>
      <i style="margin-bottom: 10px">{{ orderStateText }}</i>
      <form
        style="all: unset; display: contents"
        @submit.prevent="
            submitOrder();
          "
      >
        <div
          style="
            width: 100%;
            margin-top: 20px;
            display: flex;
            justify-content: space-around;
          "
        >
          <button
            v-if="isModifyable"
            class="delete-button"
            type="button"
            @click="
              if (id == null){
                resetOrder();
              } else {
                order.state = 'canceled';
                updateOrder(order);
              }
            "
            v-bind:disabled="id == null || !isEditableorder"
          >
            <FontAwesomeIcon :icon="faXmark" /> Anulează Aviz
          </button>
          <button
            v-if="isModifyable"
            class="submit-button"
            v-bind:disabled="!(isEditableorder && isValidorder)"
            type="submit"
          >
            <FontAwesomeIcon :icon="faCashRegister" /> Trimite la caserie
          </button>
          <button
            v-if="!isModifyable"
            class="edit-button"
            @click="
              order.state = 'in_progress';
              updateOrder(order);
            "
          >
            <FontAwesomeIcon :icon="faEdit" />Modifică
          </button>
        </div>
        <table>
          <tr>
            <th></th>
            <th>Cod</th>
            <th>Cant.</th>
            <th>Preț</th>
            <th>P. Saga</th>
          </tr>
          <ProductView
            v-for="(item, index) in order.products"
            :key="index"
            v-model:price="order.products[index].price"
            v-model:productCode="order.products[index].productCode"
            v-model:quantity="order.products[index].quantity"
            v-bind:editable="isEditableorder"
            @deleteItem="deleteProduct(index)"
            ref="productViews"
            @next="newProduct"
            @submit="submitOrder"
            @productDetailsAvailable="
              order.products[index].price = $event.productDetails.pret_v_tva;"
          />
        </table>
        <button
          style="margin-top: 10px"
          type="button"
          class="new-button"
          @click="newProduct"
          v-bind:disabled="!isEditableorder"
        >
          <FontAwesomeIcon :icon="faPlus" />
          {{ $t("label.new_product") }}
        </button>
        <span style="margin-top: 10px"
          >Total: <b>{{ total }}</b></span
        >
      </form>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "pinia";
import { useOrderStore, isBlankOrder } from "./orders";
import ProductView from "./ProductView.vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faPlus,
  faTrash,
  faCashRegister,
  faXmark,
  faEdit,
} from "@fortawesome/free-solid-svg-icons";
import OperatorNav from "./OperatorNav.vue";

export default {
  components: {
    ProductView,
    FontAwesomeIcon,
    OperatorNav,
  },
  computed: {
    isModifyable() {
      return !["submitted", "canceled"].includes(this.order.state);
    },
    total() {
      return this.order.products
        .map((p) => p.quantity * p.price)
        .reduce((s, v) => s + v, 0);
    },
    isValidorder() {
      function isValid(p) {
        return p.productCode != "" && p.quantity != "" && p.price != "";
      }

      return (
        this.order.products.length > 0 && this.order.products.every(isValid)
      );
    },
    isEditableorder() {
      return this.order.state == "in_progress";
    },
    orderStateText() {
      switch (this.order.state) {
        case "in_progress":
          return "în curs de editare";
        case "canceled":
          return "anulat";
        case "submitted":
          return "trimis la caserie";
        case "cashed":
          return "încasat";
      }
      return "";
    },
    ...mapState(useOrderStore, ["orders"]),
  },
  props: {
    id: Number,
    isCashierMode: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["orderCreated"],
  data() {
    return {
      productCode: "",
      quantity: 1,
      orderLoaded: false,
      order: {},
      faPlus,
      faTrash,
      faCashRegister,
      faXmark,
      faEdit,
    };
  },
  watch: {
    orders: {
      handler(neworders) {
        if (this.id !== null){
          this.loadOrder(neworders, this.id);
        }
      },
      deep: true, // Ensures Vue watches changes inside the array
      immediate: true, // Runs the handler immediately on component mount
    },
    id: {
      handler(to) {
        this.loadOrder(this.orders, to);
      },
      immediate: true, // Runs the handler immediately on component mount
    },
    order: {
      handler(newOrderValue) {
        if (isBlankOrder(newOrderValue)) {
          this.$nextTick(() => {
            this.$refs.productViews[0].focusProductCode();
          });
        }
      },
      deep: true,
    },
  },
  methods: {
    resetOrder() {
      this.order = {person: "", state: "in_progress", date_created: new Date().toISOString(), products: [{productCode: "", quantity: "", price: ""}]};
    },
    ...mapActions(useOrderStore, ["loadReceipts", "createDetailedOrder"]),
    submitOrder() {
      if (this.id === null) {
        this.order.state = "submitted";
        this.createDetailedOrder(this.order).then((order) => {
          this.$emit("orderCreated", order.id);
        });
        this.resetOrder();
        return;
      }
      if (!(this.isEditableorder && this.isValidorder)) {
        return;
      }
      this.order.state = "submitted";
      this.updateOrder(this.order);
    },
    loadOrder(orders, id) {
      console.log("this.order:", this.order);
      if (id === null) {
        this.resetOrder();
        this.orderLoaded = true;
        return;
      }
      const index = orders.findIndex((order) => order.id == id);
      this.order = orders[index];
      this.orderLoaded = this.order !== undefined;
    },
    ...mapActions(useOrderStore, ["updateOrder"]),
    newProduct() {
      this.order.products.push({
        productCode: "",
        quantity: "",
        price: "",
      });
      this.$nextTick(
        () => {
          this.$refs.productViews[this.order.products.length - 1].focusProductCode();
        }
      )
      this.updateOrder(this.order);
    },
    deleteProduct(index) {
      this.order.products.splice(index, 1);
      this.updateOrder(this.order);
    },
  },
  mounted() {
    if (!this.order) {
      return;
    }
    if (isBlankOrder(this.order)) {
      this.$refs.productViews[0].focusProductCode();
    }
  },
};
</script>
