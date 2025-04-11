<template>
    <nav style="width: 100%; display: flex; justify-content:space-around">
        <button @click="$router.push('/operator')">Lista avize</button>
        <button @click="onNewOrder">Aviz nou</button>
    </nav>
</template>

<script>
import { useOrderStore } from './orders'
import { mapActions } from 'pinia';
export default {
    methods: {
        onNewOrder() {
            this.createOrder("cristi").then(order => {
                this.$router.push({ name: "order", params: { id: order.id } });
            });
        },
        ...mapActions(useOrderStore, ["createOrder"]),
    }
};
</script>