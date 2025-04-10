<script>
import { mapActions } from "pinia";
import { useInvoiceStore } from "./invoices";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import ReticentUpdater from "./ReticentCaller";

export default {
  components: {
    FontAwesomeIcon
  },
  props: ["productCode", "quantity", "price", "editable"],
  emits: [
    "update:productCode",
    "update:price",
    "update:quantity",
    "deleteItem",
    "updateDescription"
  ],
  watch: {
    productCode: {
      handler(newCode) {
        this.code = newCode;
        if (this.code) {
          this.reticentCaller.trigger();
        } else {
          this.dbProduct = null;
        }
      },
      immediate: true
    }
  },
  data() {
    return {
      reticentCaller: new ReticentUpdater(200, this.getDBProduct, (product) => { this.dbProduct = product }),
      dbProduct: null,
      faTrash,
      code: null
    }
  },
  methods: {
    ...mapActions(useInvoiceStore, ["getProductByCode"]),
    async getDBProduct() {
      if (!this.code) {
        return null;
      }
      const response = await this.getProductByCode(this.code);
      const products = response.data;
      console.log("products", products);
      if (products.length != 1) {
        return null;
      }
      return products[0];
    }
  }
};
</script>

<template>
  <tr :class="dbProduct ? 'noborder' : ''">
    <td>
      <button @click="$emit('deleteItem', null)" class="delete-button small-button" v-bind:disabled="!editable">
        <FontAwesomeIcon :icon="faTrash" />
      </button>
    </td>
    <td>
      <input v-if="editable" class="productcode" type="number" v-bind:value="productCode" placeholder="Cod"
        @input="(event) => $emit('update:productCode', event.target.value)" />
      <span v-else>{{ productCode }}</span>
    </td>
    <td>
      <input v-if="editable" class="quantity" type="number" v-bind:value="quantity" placeholder="Cantitate"
        @input="(event) => $emit('update:quantity', event.target.value)" />
      <span v-else>{{ quantity }}</span>
    </td>
    <td>
      <input v-if="editable" class="price" type="number" v-bind:value="price" placeholder="Preț"
        @input="(event) => $emit('update:price', event.target.value)" />
      <span v-else>{{ price }}</span>
    </td>
    <td>
      {{ dbProduct ? dbProduct.pret_v_tva : "-" }}
    </td>
  </tr>
  <tr v-if="dbProduct">
    <td colspan="5">{{ dbProduct.name }}</td>
  </tr>
</template>