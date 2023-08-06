<template>
  <div v-if="loading" class="loading">Loading...</div>
  <div v-if="error" class="error">{{ error }}</div>
  <template v-if="curd">
    <div class="input-container" style="width: 200px">
      <label>Currency</label>
      <select name="currency" @change="calculate_gs" placeholder="Currency" >
        <option v-for="cur in currencies" :key="cur" :value="cur">
          {{ cur }}
        </option>
      </select>
    </div>
    <div class="input-container">
      <label>Date</label>
      <input name="date" type="date" value="1">
    </div>
    <div class="input-container">
      <label>Calculate your money</label>
      <input name="have_usd" @keyup.enter="calculate_gs" placeholder="I have USD" type="number" value="1000">
      <small>Press ENTER to make the calcs</small>
    </div>
    <!-- <div class="input-container-items">
    </div> -->
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Source</th>
          <th>Currency</th>
          <th>Buy</th>
          <th>Sale</th>
          <th>Gs by average</th>
          <th>Gs by buying</th>
          <th>Gs by selling</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in currency_data" :key="row.id">
          <td>{{ row.date }}</td>
          <td>{{ row.source }}</td>
          <td>{{ row.currency }}</td>
          <td>{{ row.buy_repr }}</td>
          <td>{{ row.sales_repr }}</td>
          <td>{{ row.gs }}</td>
          <td>{{ row.gs_buying }}</td>
          <td>{{ row.gs_selling }}</td>
        </tr>
      </tbody>
    </table>
  </template>
</template>
<script setup>
import { ref } from 'vue';
import { get_group_exchanges, 
         formatCurrency, 
         get_currencies,
         get_last_day
         } from 'modules/j_exchange';

const props = defineProps({
  currencies: { type: Array, required: true },
  edate: String
})

const curd = ref(null)
const loading = ref(true);
const error = ref(null);

const currencies = ref([]);

const currency_data = ref([]);


const data = {
  'criteria': [
    {
      attr: "source",
      optr: "==",
      value: "SET"
    },
    {
      attr: "currency",
      optr: "==",
      value: "USD"
    },
  ],
  'limit': 10,
  'order_by': ['-date', 'source'],
};

get_last_day().then((rsp)=>{
  if (!rsp) {
    error.value = `The value from the server is null ${rsp}`;
  }
  loading.value = false;
  curd.value = true;
  return rsp
}).then((rsp)=>{
  document.querySelector('input[name=date]').value = rsp.data;
  get_currencies().then(rsp=>{
    rsp.data.forEach((ii)=>{
      currencies.value.push(ii)
    })
  }).then(()=>{
      calculate_gs();
    })
});

const calculate_gs = () => {
  currency_data.value = [];
  loading.value = true;
  let tf = 2;
  let gs_val = document.querySelector('input[name=have_usd]').value;
  let date = document.querySelector('input[name=date]').value;
  let currency = document.querySelector('select[name=currency]').value;
  get_group_exchanges(date, currency, loading).then((rsp)=>{
    if (!rsp) {
      error.value = `The value from the server is null ${rsp}`;
    }
    loading.value = false
    rsp.data.forEach((itobj) => {
      //let gs_avg = ((itobj.buy + itobj.sales) / 2) * gs_val;
      let gs_avg = itobj.average * gs_val;
      let gs_buying = itobj.buy * gs_val;
      let gs_selling = itobj.sales * gs_val;
      currency_data.value.push({
        id: itobj.id,
        date: new Date(itobj.date).toISOString().split('T')[0],
        source: itobj.source,
        currency: itobj.currency,
        buy_repr: formatCurrency(itobj.buy),
        sales_repr: formatCurrency(itobj.sales),
        buy: itobj.buy,
        sales: itobj.sales,
        gs: formatCurrency(Number(gs_avg.toFixed(tf))),
        gs_buying: formatCurrency(Number(gs_buying.toFixed(tf))),
        gs_selling: formatCurrency(Number(gs_selling.toFixed(tf))),
      })
    })
    curd.value = true;
  })
}




</script>
