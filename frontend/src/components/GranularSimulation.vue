<template>
  <div class="container">
    <div class="row">
      <div class="col mt-3">
        <h4>Guided practice</h4>
        <!-- <b>Step 1: Asking Clarifying Question</b> -->
        <!-- Floating Icon and Popup above the languageSelect -->
        <div class="icon-container mt-2">
          <!-- Floating Icon -->
          <div class="floating-icon" @click="togglePopup">
            <i class="fas fa-comments"></i>
          </div>

          <!-- Popup message (to the right of the icon) -->
          <div v-if="showPopup" class="popup-message">
            <p>{{ popupMessage }}</p>

            <div v-if="currState.value==PracticeState.Practicing" class="mt-3">
              <p>After practicing this section, click get feedback to get immediate feedback</p>
              <button class="btn btn-outline-primary mt-1" style="font-size: 90%;">Get Feedback</button>

            </div>
          </div>

          
        </div>

        <div class="form-group mt-3">
          <select id="languageSelect" class="form-select" v-model="selectedLanguage" @change="updateLanguage">
            <option value="python">Python</option>
            <option value="java">Java</option>
            <option value="cpp">C++</option>
            <option value="javascript">JavaScript</option>
            <!-- Add more languages as needed -->
          </select>
        </div>

        <codemirror v-model="code" placeholder="" :style="{ height: '60vh' }" :autofocus="true" :indent-with-tab="true" style="max-width:38rem; font-size: smaller;"
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

const PracticeState = {
  NotStarted: -1,
  Practicing: 0,
  FeedbackReceived: 1
}

export default defineComponent({
  components: {
    Codemirror,
    ChatboxSimulation
  },
  setup() {
    const code = ref(``)
    const selectedLanguage = ref('python')
    const extensions = ref([python(), oneDark])

    const view = shallowRef()
    const showPopup = ref(true) // Control popup visibility
    const popupMessage = ref("Let's start the practice by clicking the start session")
    const listStep = ["Clarification", "Proposing Solution"]
    const listMessage = ["Try to ask clarifying questions", "Try to explain your approach"]
    const startStopIdxForFeedback = ref([1,1])
    const currentStepIdx = ref(-1)
    const currState = ref(PracticeState.NotStarted) // -1 not started, 0 start and currently practicing (show feedback button), 1 after get feedback (show retry or next section).

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

    const togglePopup = () => {
      showPopup.value = !showPopup.value
      // Auto-hide popup after 3 seconds
      // if (showPopup.value) {
      //   setTimeout(() => {
      //     showPopup.value = false
      //   }, 3000)
      // }
    }

    return {
      code,
      selectedLanguage,
      extensions,
      handleReady,
      updateLanguage,
      showPopup,  // Added showPopup reactive property
      togglePopup,
      log: console.log,
      popupMessage,
      currState,
      PracticeState
    }
  }
})
</script>

<style>
.form-select {
  max-width: 25%;
}

/* Container for the icon and popup message */
.icon-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

/* Floating Icon */
.floating-icon {
  background-color: #007bff;
  color: white;
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.3);
  margin-right: 10px;
}

.floating-icon i {
  font-size: 24px;
}

.floating-icon:hover {
  background-color: #0056b3;
}

/* Popup message to the right of the icon */
.popup-message {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 10px 15px;
  border-radius: 10px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.3);
  font-size: 14px;
  width: 400px;
  transition: opacity 0.3s ease;
  white-space: wrap;
}

.popup-message p {
  margin: 0;
}
</style>