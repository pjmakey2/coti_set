<script setup>
import { ref, onMounted } from 'vue';
import Pivot from "../components/Pivot.vue"
import "webdatarocks/webdatarocks.css";

const toolbarv = ref(true);
const g_exc = ref(null)

function gridExchanges() {
    const data = {
        'criteria': [
            {
                attr: "date",
                optr: "==",
                value: "2023-06-01"
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
            //loading.value = false;
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes("application/json")) {
                msge = "Oops, we haven't got JSON!"
                //error.value = msge;
                throw new TypeError(msge);
            }
            return response.json()
        })
        .then(rsp => {
            if (!rsp) {
                //error.value = `The value from the server is null ${rsp}`;
            }
            if (rsp.hasOwnProperty('detail')) {
                //error.value = rsp.detail[0].msg;
            }
            if (rsp.hasOwnProperty('data')) {
                //console.log(rsp.data);
                g_exc.value = {
                    dataSource: {
                        data:rsp.data
                    }
                }
                console.log(g_exc.value, 'data ???')
                //createData();
            }
        }).catch(error => {
            //error.value = error;
            console.log('Error:', error);
        });

}

function customizeToolbar(ttv) {
    var tabs = ttv.getTabs(); // get all tabs from the ttv
    ttv.getTabs = function () {
        delete tabs[0];
        delete tabs[1];
        delete tabs[2];
        return tabs;
    }
}

onMounted(() => {
  gridExchanges();
})

</script>
<template>
    <Pivot v-if="g_exc" :beforetoolbarcreated="customizeToolbar" :toolbar="toolbarv" :report="g_exc" />
</template>