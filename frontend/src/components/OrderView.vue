<template>
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
</template>

export default {
    props: {
        order: {
            type: Object,
            required: true,
        }
    },
    methods: {
        newProduct() {
            this.order.products.push({
                productCode: "",
                quantity: "",
                price: "",
            });
            this.$nextTick(() => {
                this.$refs.productViews[this.order.products.length - 1].focusProductCode();
            });
        },
        deleteProduct(index) {
            this.order.products.splice(index, 1);
        },
        submitOrder() {
            this.$emit('submitOrder');
        }
    },
}