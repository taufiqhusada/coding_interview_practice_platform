<template>
  <div class="container">
    <div class="row">

      <div class="col mt-3">
        <div class="form-group">
          <select id="languageSelect" class="form-select" v-model="selectedLanguage" @change="updateLanguage">
            <option value="python">Python</option>
            <option value="java">Java</option>
            <option value="cpp">C++</option>
            <option value="javascript">JavaScript</option>
            <!-- Add more languages as needed -->
          </select>
        </div>
        <codemirror v-model="code" placeholder="" :style="{ height: '78vh' }" :autofocus="true" :indent-with-tab="true" style="max-width:38rem; font-size: smaller;"
          :tab-size="2" :extensions="extensions" @ready="handleReady" @change="log('change', $event)"
          @focus="log('focus', $event)" @blur="log('blur', $event)" />
      </div>
      <div class="col">
        <ChatboxSimulation :code="code"></ChatboxSimulation>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, shallowRef } from 'vue'
import { Codemirror } from 'vue-codemirror'
import { javascript } from '@codemirror/lang-javascript'
import { python } from '@codemirror/lang-python'
import { java } from '@codemirror/lang-java'
import { cpp } from '@codemirror/lang-cpp'
import { oneDark } from '@codemirror/theme-one-dark'
import { EditorState, Compartment } from '@codemirror/state'
import hljs from 'highlight.js';
import ChatboxSimulation from './ChatboxSimulation.vue';

export default defineComponent({
  components: {
    Codemirror,
    ChatboxSimulation
  },
  setup() {
    const code = ref(``)
    const selectedLanguage = ref('python')
    const extensions = ref([javascript(), oneDark])

    // Codemirror EditorView instance ref
    const view = shallowRef()

    const handleReady = (payload) => {
      view.value = payload.view
    }

    const languages = {
      
      python: python(),
      java: java(),
      cpp: cpp(),
      javascript: javascript(),
    }


    const updateLanguage = () => {
      const newExtension = languages[selectedLanguage.value]
      extensions.value = [newExtension, oneDark]
    }

    return {
      code,
      selectedLanguage,
      extensions,
      handleReady,
      updateLanguage,
      log: console.log
    }
  }
})
</script>

<style>
.form-select{
  max-width: 25%;
}
</style>
