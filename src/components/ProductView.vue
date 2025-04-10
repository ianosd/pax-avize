<script>
import { mapActions } from "pinia";
import { useInvoiceStore } from "./invoices";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faTrash } from '@fortawesome/free-solid-svg-icons';

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
  data() {
    return {
      dbProduct: null,
      faTrash
    }
  },
  methods: {
    ...mapActions(useInvoiceStore, ["getProductByCode"]),
    updateProductInfo(code) {
      // TODO optimize
      console.log("updating code");
      if (!code) {
        this.dbProduct = null;
        return;
      }
      this.getProductByCode(code).then(response => {
        const products = response.data;
        console.log("products", products);
        if (products.length != 1) {
          this.dbProduct = null;
          return;
        }
        const product = products[0];
        if (product.cod == this.productCode) {
          console.log("updating Product", product);
          this.dbProduct = product;
        } else {
          this.dbProduct = null;
        }
      })
    }
  }
};
</script>

<template>
  <tr :class="dbProduct?'noborder':''">
    <td>
      <button @click="$emit('deleteItem', null)" class="delete-button small-button" v-bind:disabled="!editable">
        <FontAwesomeIcon :icon="faTrash" />
      </button>
    </td>
    <td>
      <input v-if="editable" class="productcode" type="number" v-bind:value="productCode" placeholder="Cod"
        @input="(event) => { $emit('update:productCode', event.target.value); updateProductInfo(event.target.value); }" />
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