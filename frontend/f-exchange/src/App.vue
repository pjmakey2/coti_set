<script setup>
import "./assets/main.css";
import { RouterLink } from 'vue-router'
import ExchangeView from './views/ExchangeView.vue'
</script>

<template>
  <header>
    <img src="@/assets/exchange.png" width="64" height="64">
    <h1>
      Currency Exchange Site
    </h1>
  </header>
  <nav>
    <ul>
      <li>
        <RouterLink to="/exchanges">Exchanges</RouterLink>
      </li>
      <li>
        <RouterLink to="/suscribe">Suscribe</RouterLink>
      </li>
      <li>
        <RouterLink to="/api_docs">API Docs</RouterLink>
      </li>
      <li>
        <a href="https://github.com/pjmakey2/coti_set" target="_blank">The code</a>
      </li>
    </ul>
  </nav>
  <section>
    <router-view>
      <ExchangeView></ExchangeView>
    </router-view>
  </section>
  <footer>
    <p>&copy; 2023 Currency Exchange Website. Created by <a href="https://github.com/pjmakey2" target="_blank">pjmakey</a></p>
  </footer>

  <!-- <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>

  </header>
  <RouterView />
  <hr>
  <ExchangeChart></ExchangeChart> -->
</template>


