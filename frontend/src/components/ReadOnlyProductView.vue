<script>
import { mapActions } from "pinia";
import { useOrderStore } from "./orders";
import ReticentUpdater from "./ReticentCaller";

export default {
  props: ["productCode", "quantity", "price"],
  computed: {
    productName() {
      const name = this.dbProduct?.name;
      if (!name) {
        return "";
      }
      if (name.length > 8) {
        return name.substring(0, 5) + "...";
      }
      return name;
    },
    productCodeStr() {
        const name =  this.dbProduct?.name;
        if (!name) {
          return this.productCode;
        } else {
            return `(${this.productCode})`;
        }
    }
  },
  data() {
    return {
      reticentCaller: new ReticentUpdater(200, this.getUniqueProductByCode, (product) => { this.dbProduct = product }),
      dbProduct: null
    };
  },
  watch: {
    productCode: {
      handler(newCode) {
        if (newCode) {
          this.reticentCaller.triggerUpdate(newCode);
        } else {
          this.dbProduct = null;
        }
      },
      immediate: true
    }
  },
  methods: {
    ...mapActions(useOrderStore, ["getUniqueProductByCode"]),
    
  }
};
</script>

<template>
  <tr :class="dbProduct ? 'noborder' : ''">
    <td>
      <span>{{ productName }}</span><br><span>{{ productCodeStr }}</span>
    </td>
    <td>
      <span>{{ quantity }} </span>
    </td>
    <td>
      <span>{{ price }}</span>
    </td>
    <td><span>{{ price*quantity }}</span></td>
  </tr>
</template>