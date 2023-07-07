<template>
    <table>
      <thead>
        <tr>
          <th>Source</th>
          <th>Currency</th>
          <th>Buy</th>
          <th>Sale</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in currency_data" :key="row.id">
          <td>{{ row.source }}</td>
          <td>{{ row.currency }}</td>
          <td>{{ row.buy }}</td>
          <td>{{ row.sale }}</td>
        </tr>
      </tbody>
    </table>
  </template>
<script setup>
    import { ref } from 'vue';
    const props = defineProps({
        currencies: {type: Array, required: true },
        edate: String
    })

    const currency_data = [{source: 'SET', currency: 'USD', buy: '1500', sale: '15000'}];

</script>
