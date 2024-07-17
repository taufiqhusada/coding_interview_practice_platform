import './assets/base.css'

// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


import { createApp } from 'vue';
import App from './App.vue';
import firebase from 'firebase/app';
import 'firebase/storage';

import { basicSetup } from 'codemirror'
import VueCodemirror from 'vue-codemirror'


import router from './router';

const app = createApp(App);
app.use(router);

app.use(VueCodemirror, {
    // optional default global options
    autofocus: true,
    disabled: false,
    indentWithTab: true,
    tabSize: 2,
    placeholder: 'Code goes here...',
    extensions: [basicSetup]
    // ...
  })

app.mount('#app');



