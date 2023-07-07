<script setup>
import { ref } from 'vue';
import ExchangeChart from '../components/ExchangeChart.vue';
import ExchangeTable from '../components/ExchangeTable.vue';

const currencies = ref(['USD']);

</script>
<template>
    <ExchangeChart></ExchangeChart>
    <hr>
    <h2 class="title">Grid Exchange of the day</h2>
    <ExchangeTable
    :currencies="currencies"
    ></ExchangeTable>
</template>