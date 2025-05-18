<script>
import { mapActions } from "pinia";
import { useOrderStore } from "./orders";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import ReticentUpdater from "./ReticentCaller";

export default {
  components: {
    FontAwesomeIcon,
  },
  computed:
  {
    priceClass() {
          return Math.abs(this.price - (this.dbProduct?.pret_v_tva)) > 0.00001 ?? false
            ? 'low-price price' 
            : 'price';
        }
  },
  props: ["productCode", "quantity", "price", "editable"],
  emits: [
    "update:productCode",
    "update:price",
    "update:quantity",
    "deleteItem",
    "updateDescription",
    "next",
    "productDetailsAvailable",
    "submit"
  ],
  watch: {
    productCode: {
      handler(newCode) {
        if (newCode) {
          this.reticentCaller.triggerUpdate(newCode);
        } else {
          this.dbProduct = null;
        }
      },
      // TODO move the initial dbProduct setup to onMounted, or even better, inside the product store, so that it is fetched only once
      immediate: true,
    },
  },
  data() {
    return {
      reticentCaller: new ReticentUpdater(
        200,
        this.getUniqueProductByCode,
        (product) => {
          this.dbProduct = product;
          if (product) {
            this.$emit("productDetailsAvailable", {
              productDetails: product
            });
          }
        }
      ),
      dbProduct: null,
      faTrash,
    };
  },
  methods: {
    ...mapActions(useOrderStore, ["getUniqueProductByCode"]),
    focusProductCode() {
      this.$refs.productCodeInput.focus();
    },
  },
};
</script>

<template>
  <tr :class="dbProduct ? 'noborder' : ''">
    <td>
      <button
        type="button"
        @click="
          $emit('deleteItem', null);
        "
        class="delete-button small-button"
        v-bind:disabled="!editable"
      >
        <FontAwesomeIcon :icon="faTrash" />
      </button>
    </td>
    <td>
      <input
        ref="productCodeInput"
        v-if="editable"
        class="productcode"
        type="number"
        v-bind:value="productCode"
        placeholder="Cod"
        @input="(event) => $emit('update:productCode', event.target.value)"
      />
      <span v-else>{{ productCode }}</span>
    </td>
    <td>
      <input
        v-if="editable"
        class="quantity"
        type="number"
        v-bind:value="quantity"
        placeholder="Cantitate"
        @input="(event) => $emit('update:quantity', event.target.value)"
      />
      <span v-else>{{ quantity }}</span>
    </td>
    <td>
      <input
        v-if="editable"
        type="number"
        v-bind:value="price"
        placeholder="Preț"
        :class="priceClass"
        @input="(event) => $emit('update:price', event.target.value)"
        @keypress="
          (event) => {
        if (event.key === 'Enter') {
          event.preventDefault();
          $emit('next');
        }
        if (event.key === ' ') {
          event.preventDefault();
          $emit('submit');
        }
          }
        "
      />
      <span v-else>{{ price }}</span>
    </td>
    <td>
      {{ dbProduct ? dbProduct.pret_v_tva : "-" }}
    </td>
  </tr>
  <tr v-if="dbProduct">
    <td colspan="5" >
      <div style="display: flex; justify-content: center; gap: 10px">
      <span>{{ dbProduct.name }}</span>
      <span
        > <b>Stoc:</b> <i>{{ dbProduct.stoc }}</i></span>
      </div>
    </td>
  </tr>
</template>