<template>
  <div v-if="loading" class="loading">Loading...</div>
  <div v-if="error" class="error">{{ error }}</div>
  <template v-if="curd">
    <div class="grid">
      <div class="column">
        <div class="input-container">
          <label>Calculate your USD</label>
          <input name="have_usd" @keyup.enter="calculate_gs" placeholder="I have USD" type="number" value="1">
          <small>Press ENTER to make the calcs</small>
        </div>
      </div>
      <!--  --><div class="column" style="flex: none; min-width: 0;max-width: none;" >
          <div class="input-container">
            <label>Average</label>
            <input @change="calculate_gs" id="average" name="type_calc" checked type="radio">
          </div>
      </div>
      <div class="column" style="flex: none; min-width: 0;max-width: none;" >
          <div class="input-container">
            <label>Buying</label>
            <input @change="calculate_gs" id="buy" name="type_calc"  type="radio">
          </div>
      </div>
      <div class="column" style="flex: none; min-width: 0;max-width: none;" >
          <div class="input-container">
            <label>Selling</label>
            <input @change="calculate_gs" id="sale" name="type_calc" type="radio">
          </div>
      </div>
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
          <th>Gs</th>
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
        </tr>
      </tbody>
    </table>
  </template>
</template>
<script setup>
import { ref } from 'vue';
import { get_exchange, formatCurrency } from 'modules/j_exchange';




const props = defineProps({
  currencies: { type: Array, required: true },
  edate: String
})

const curd = ref(null)
const loading = ref(true);
const error = ref(null);

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

get_exchange(data, loading).then((rsp) => {
  if (!rsp) {
    error.value = `The value from the server is null ${rsp}`;
  }
  loading.value = false
  rsp.data.forEach((itobj) => {
    currency_data.value.push({
      id: itobj.id,
      date: new Date(itobj.date).toLocaleDateString('en-gb'),
      source: itobj.source,
      currency: itobj.currency,
      buy_repr: formatCurrency(itobj.buy),
      sales_repr: formatCurrency(itobj.sales),
      buy: itobj.buy,
      sales: itobj.sales,
      gs: 0,
    })
  })
  curd.value = true;
  
});

const calculate_gs = () => {
  let gs_val = document.querySelector('input[name=have_usd]').value;
  let average = document.querySelector('#average')
  let buy = document.querySelector('#buy')
  let sale = document.querySelector('#sale')
  console.table(average.checked,
    buy.checked,
    sale.checked,
  )
  for (let idx in currency_data.value) {
    if (average.checked) {
      let v = ((currency_data.value[idx].buy + currency_data.value[idx].sales) / 2) * gs_val
      currency_data.value[idx].gs = formatCurrency(Number(v.toFixed(2)));
    } 
    if (buy.checked) {
      let v = currency_data.value[idx].buy * gs_val
      currency_data.value[idx].gs = formatCurrency(Number(v.toFixed(2)));
    }     
    if (sale.checked) {
      let v = currency_data.value[idx].sales * gs_val
      currency_data.value[idx].gs = formatCurrency(Number(v.toFixed(2)));
    }
  }
}

</script>
