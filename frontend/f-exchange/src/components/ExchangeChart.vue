<template>
  <div v-if="loading" class="loading">Loading...</div>
  <div v-if="error" class="error">{{ error }}</div>
  <v-chart class="chart" :option="options" />
</template>
  
<script setup>
import { ref, onMounted, provide } from 'vue'
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";

use([CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent]);

provide(THEME_KEY, "light");

const loading = ref(true);
const post = ref([]);
const error = ref(null);
const options = ref({});

function getExchanges() {
  const data = {
    'criteria': [
    {
      attr: "group_source",
      optr: "==",
      value: "bcp"
    },
    // {
    //   attr: "month",
    //   optr: "==",
    //   value: "6"
    // }        
    // {
    //   attr: "source",
    //   optr: "==",
    //   value: "SET"
    // },    
    ],
    'order_by': ['date', 'source']
  };
  const model = { module: 'models.m_finance', model: 'Exchange' }
  const mp = new URLSearchParams(model);

  const url = `${import.meta.env.VITE_API_URL}/${import.meta.env.VITE_API_VERSION}/${import.meta.env.VITE_API_RT}/${import.meta.env.VITE_API_QS}?${mp}`;
  // const url = 'lelo'

  fetch(url, {
    method: 'POST',
    cache: 'no-cache',
    headers: {
      "accept": 'application/json',
      "Content-Type": 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => {
      loading.value = false;
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes("application/json")) {
        msge = "Oops, we haven't got JSON!"
        error.value = msge;
        throw new TypeError(msge);
      }
      return response.json()
    })
    .then(rsp => {
      if (!rsp) {
        error.value = `The value from the server is null ${rsp}`;
      }
      if (rsp.hasOwnProperty('detail')) {
        error.value = rsp.detail[0].msg;
      }
      if (rsp.hasOwnProperty('data')) {
        //console.log(rsp.data);
        post.value = rsp.data;
        createData();
      }
    });
  // .catch(error => {
  //   error.value = error;
  //   console.log('Error:', error);
  // });
}

function createData() {
  const dateList = post.value.map((item) => item.date)
  //const seriesList = post.value.map((item) => item.sales)
  const datasetWithFilters = [];
  const seriesList = [];
  const currencies = new Set(post.value.map((item) => item.currency));
  currencies.forEach((sso) => {
    let did = `dataset_${sso}`;
    datasetWithFilters.push({
      id: did,
      fromDatasetId: 'dataset_raw',
      transform: {
        type: 'filter',
        config: {
          and: [
            { dimension: 'currency', '=': sso }
          ]
        }
      }
    });
    seriesList.push({
      type: 'line',
      datasetId: did,
      showSymbol: true,
      symbolSize: 8,
      name: sso,
      // sampling: 'lttb',
      // stack: 'Total',
      // stackStrategy: 'samesign',
      // smooth: true,
      //step: 'start',
      // endLabel: {
      //   show: true,
      //   formatter: function (params) {
      //     return params.value[3] + ': ' + params.value[0];
      //   }
      // },
      labelLayout: {
        moveOverlap: 'shiftY'
      },
      emphasis: {
        focus: 'series'
      },
      encode: {
        x: 'date',
        y: 'sales',
        label: ['source', 'sales'],
        itemName: 'date',
        tooltip: ['sales']
      }
    });

  })
  options.value = {
    animationDuration: 10000,
    dataset: [
      {
        id: 'dataset_raw',
        source: post.value
      },
      ...datasetWithFilters
    ],
    title: {
      left: 'center',
      text: 'Currency data of Paraguay'
    },
    tooltip: {
      order: 'valueDesc',
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      // nameLocation: 'middle'
    },
    yAxis: {
      name: 'Vta',
    },
    grid: {
      right: 140
    },
    series: seriesList
  };
}

onMounted(() => {
  getExchanges();
})


// Make the GET request using fetch


// import { use } from "echarts/core";
// import { CanvasRenderer } from "echarts/renderers";
// import { PieChart } from "echarts/charts";o
// import {
//     TitleComponent,
//     TooltipComponent,
//     LegendComponent
// } from "echarts/components";
// import VChart, { THEME_KEY } from "vue-echarts";
// import { ref, provide } from "vue";

// use([
//     CanvasRenderer,
//     PieChart,
//     TitleComponent,
//     TooltipComponent,
//     LegendComponent
// ]);

// provide(THEME_KEY, "dark");

// const option = ref({
//     title: {
//         text: "Traffic Sources",
//         left: "center"
//     },
//     tooltip: {
//         trigger: "item",
//         formatter: "{a} <br/>{b} : {c} ({d}%)"
//     },
//     legend: {
//         orient: "vertical",
//         left: "left",
//         data: ["Direct", "Email", "Ad Networks", "Video Ads", "Search Engines"]
//     },
//     series: [
//         {
//             name: "Traffic Sources",
//             type: "pie",
//             radius: "55%",
//             center: ["50%", "60%"],
//             data: [
//                 { value: 335, name: "Direct" },
//                 { value: 310, name: "Email" },
//                 { value: 234, name: "Ad Networks" },
//                 { value: 135, name: "Video Ads" },
//                 { value: 1548, name: "Search Engines" }
//             ],
//             emphasis: {
//                 itemStyle: {
//                     shadowBlur: 10,
//                     shadowOffsetX: 0,
//                     shadowColor: "rgba(0, 0, 0, 0.5)"
//                 }
//             }
//         }
//     ]
// });
</script>
  
<style scoped>
.chart {
  height: 400px;
}
</style>