<script>
export default {
  props: ["productCode", "quantity", "price", "valid", "editable"],
  emits: [
    "update:productCode",
    "update:price",
    "update:quantity",
    "update:valid",
  ],
  computed: {
    isValidable() {
      return this.productCode != "" && this.quantity != "" && this.price != "";
    },
  },
};
</script>

<template>
  <td>
    <input
      v-if="!valid && editable"
      class="productcode"
      type="number"
      v-bind:value="productCode"
      placeholder="Product Code"
      @input="(event) => $emit('update:productCode', event.target.value)"
    />
    <span v-else>{{ productCode }}</span>
  </td>
  <td>
    <input
      v-if="!valid && editable"
      class="quantity"
      type="number"
      v-bind:value="quantity"
      placeholder="Quantity"
      @input="(event) => $emit('update:quantity', event.target.value)"
    />
    <span v-else>{{ quantity }}</span>
  </td>
  <td>
    <input
      v-if="!valid && editable"
      class="price"
      type="number"
      v-bind:value="price"
      placeholder="Price"
      @input="(event) => $emit('update:price', event.target.value)"
    />
    <span v-else>{{ price }}</span>
  </td>
  <td>
    <input
      v-bind:checked="valid"
      type="checkbox"
      v-bind:disabled="!isValidable || !editable"
      @input="(event) => {$emit('update:valid', event.target.checked);}"
    />
  </td>
</template>