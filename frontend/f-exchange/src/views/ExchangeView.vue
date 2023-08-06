<template>
    <ExchangeChart></ExchangeChart>
    <hr>
    <h2 class="title">Grid Exchange of the day</h2>
    <ExchangeTable
    :currencies="currencies"
    ></ExchangeTable>
</template>
<script setup>
import { ref } from 'vue';
import ExchangeChart from '../components/ExchangeChart.vue';
import ExchangeTable from '../components/ExchangeTable.vue';
import { get_group_exchanges } from 'modules/j_exchange';

const currencies = ref(['USD']);

const loading = ref(false);

get_group_exchanges('2023-08-01', 'USD', loading);

</script>