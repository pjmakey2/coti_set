<template>
  <div v-if="loading" class="loading">Loading...</div>
  <div v-if="error" class="error">{{ error }}</div>
  <table v-if="curd">
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
import get_exchange from 'modules/j_exchange';

const props = defineProps({
  currencies: { type: Array, required: true },
  edate: String
})

const curd = ref(null)
const loading = ref(true);
const error = ref(null);

const currency_data = [{ source: 'SET', currency: 'USD', buy: '1500', sale: '15000' }];

const data = {
  'criteria': [
    {
      attr: "group_source",
      optr: "==",
      value: "set"
    },
  ],
  'order_by': ['date', 'source']
};

</script>
