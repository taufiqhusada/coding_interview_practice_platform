<template>
  <div class="container">
    <div class="row">
      <div class="col mt-3">
        <!-- <h4>Guided practice</h4> -->
        <!-- <b>Step 1: Asking Clarifying Question</b> -->
        <!-- Floating Icon and Popup above the languageSelect -->
        <div class="icon-container mt-2">
          <!-- Floating Icon -->
          <div class="floating-icon" @click="togglePopup">
            <i class="fas fa-comments"></i>
          </div>

          <!-- Popup message (to the right of the icon) -->
          <div v-if="showPopup" class="popup-message">
            <loader_simple v-if="currState == PracticeState.WaitingForFeedback"
              style="margin-left: 20px;"></loader_simple>
            <div v-else>
              <div v-show="currState != PracticeState.NotStarted">
                <b>Step {{ currentStepIdx + 1 }} : {{ listStep[currentStepIdx] }}</b>
              </div>

              <p>{{ popupMessage }}</p>
              <div v-show="currState == PracticeState.Practicing" class="mt-3">
                <p>After practicing this step, click get feedback button to get immediate feedback</p>
                <button class="btn btn-outline-primary mt-1" style="font-size: 90%;" @click="getFeedback">Get
                  Feedback</button>
              </div>
              <div v-show="currState == PracticeState.FeedbackReceived" class="mt-3">
                <p>Do you want to try again this step or go to next step?</p>
                <button class="btn btn-outline-primary mt-1" style="font-size: 90%;" @click="retry">Retry</button>
                <button class="btn btn-outline-primary mt-1" style="font-size: 90%; margin-left: 20px;"
                  @click="nextStep">Next Step</button>
              </div>
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

        <codemirror v-model="code" placeholder="" :style="{ height: '60vh' }" :autofocus="true" :indent-with-tab="true"
          style="max-width:38rem; font-size: smaller;" :tab-size="2" :extensions="extensions" @ready="handleReady"
          @change="log('change', $event)" @focus="log('focus', $event)" @blur="log('blur', $event)" />
      </div>

      <div class="col">
        <ChatboxSimulation ref="chatboxSimRef" :code="code" @update:PracticeState="updatePracticeState">
        </ChatboxSimulation>
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
import axios from 'axios';
import loader_simple from './misc/loader_simple.vue'

const PracticeState = {
  NotStarted: -1,
  Practicing: 0,
  FeedbackReceived: 1,
  WaitingForFeedback: 2,
}

export default defineComponent({
  components: {
    Codemirror,
    ChatboxSimulation,
    loader_simple
  },
  setup() {
    const code = ref(``)
    const selectedLanguage = ref('python')
    const extensions = ref([python(), oneDark])

    const view = shallowRef()
    const showPopup = ref(true) // Control popup visibility
    const popupMessage = ref("Ready to start? Click the start session button to begin your practice session!")

    const listStep = ["Understanding", "Initial Ideation", "Idea Justification", "Implementation", "Review (Dry Run)", "Evaluation"]

    const listMessage = [
      "Start by asking a few clarifying questions and suggesting a test case to show your understanding.",
      "Share some initial ideas on how you might approach solving the problem.",
      "Explain why you chose this approach and why it works for the problem.",
      "Begin coding and talk through each step as you work through the solution.",
      "Walk through your code with a test case to ensure it runs as expected.",
      "Review your solution and consider any improvements or edge cases you might have missed."
    ]

    let prevLastInterviewerChatIdx = 0
    const currentStepIdx = ref(-1)
    const currState = ref(PracticeState.NotStarted) // -1 not started, 0 start and currently practicing (show feedback button), 1 after get feedback (show retry or next section).

    const chatboxSimRef = ref(null);
    const chatMessages = ref([]);

    const backendURL = "/api"

    console.log(currState)
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

    const updatePracticeState = (state) => {
      currState.value = state;

      currentStepIdx.value += 1
      popupMessage.value = listMessage[currentStepIdx.value]
    }

    const getFeedback = async () => {
      currState.value = PracticeState.WaitingForFeedback;
      if (chatboxSimRef.value) {
        chatMessages.value = chatboxSimRef.value.getTranscriptSession();  // Call the function
        // save 
        try {
          // Make a POST request to your API
          const requestBody = {
            transcript: chatMessages.value.slice(prevLastInterviewerChatIdx),
            phase: listStep[currentStepIdx.value]
          };
          const response = await axios.post(`${backendURL}/getFeedback/specific`, requestBody);
          if (response.status === 200) {
            // Update the feedback field with the response from GPT-4
            console.log(response.data)

            const feedback = response.data["feedback"]

            currState.value = PracticeState.FeedbackReceived;
            popupMessage.value = feedback;

          } else {
            // Handle API response error
            console.error('Failed to save and get feedback', response.status, response.data);
          }
        } catch (error) {
          // Handle network or other errors
          console.error('Error while saving and get feedback', error);
        }



      }
    };

    const retry = () => {
      // TODO: reset transcript
      console.log(prevLastInterviewerChatIdx);
      chatboxSimRef.value.clearTranscriptSession(prevLastInterviewerChatIdx + 1);

      popupMessage.value = listMessage[currentStepIdx.value];
      currState.value = PracticeState.Practicing;
    };

    const nextStep = () => {
      currentStepIdx.value += 1;
      popupMessage.value = listMessage[currentStepIdx.value];


      prevLastInterviewerChatIdx = chatMessages.value.length-1;
      if (chatMessages.value[chatMessages.value.length-1].role == "interviewee" ){
        prevLastInterviewerChatIdx -= 1;
      }

      currState.value = PracticeState.Practicing;

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
      PracticeState,
      updatePracticeState,
      chatboxSimRef,
      getFeedback,
      retry,
      nextStep,
      listStep,
      currentStepIdx
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