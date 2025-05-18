<script>
import { mapActions } from "pinia";
import { useOrderStore } from "./orders";
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
        if (newCode) {
          this.reticentCaller.triggerUpdate(newCode);
        } else {
          this.dbProduct = null;
        }
      },
      // TODO move the initial dbProduct setup to onMounted, or even better, inside the product store, so that it is fetched only once
      immediate: true
    }
  },
  data() {
    return {
      reticentCaller: new ReticentUpdater(200, this.getUniqueProductByCode, (product) => { this.dbProduct = product }),
      dbProduct: null,
      faTrash
    }
  },
  methods: {
    ...mapActions(useOrderStore, ["getUniqueProductByCode"]),
    focusProductCode() {
      console.log("Focusing product code input");
      this.$refs.productCodeInput.focus();
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
      <input ref="productCodeInput" v-if="editable" class="productcode" type="number" v-bind:value="productCode" placeholder="Cod"
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
    <td colspan="5"><span>{{ dbProduct.name }}</span> <span><label> <b>Stoc:</b> </label></span> <i>{{ dbProduct.stoc }}</i></td>
  </tr>
</template>