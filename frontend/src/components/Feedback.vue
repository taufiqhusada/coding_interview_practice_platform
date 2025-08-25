<template>
  <div class="mt-3" v-if="transcript.length !== 0">
    <div class="row">
      <div class="col-sm-4">

        <section ref="chatArea" class="transcript">
          <h5 class="headline">Transcript</h5>
          <div class="mt-2">

          </div>
          <div v-for="(message, index) in transcript" :key="index"
            :class="[{ 'margin-right': message.role === 'interviewer', 'margin-left': message.role === 'interviewee' }]">
            <div class="message-container">
              <div class="content">
                <span
                  :class="[{ 'speaker-1': message.role === 'interviewee', 'speaker-2': message.role === 'interviewer' }]">
                  <b>{{ message.role }}:</b>
                </span>
                {{ message.content }}
              </div>
            </div>
          </div>
        </section>
      </div>

      <div class="col-sm-8">
        <section ref="chatArea" class="transcript">
          <h5 class="headline">Assessment of the Think-Aloud Process</h5>

          <div class="message-container mt-2">
            <div class="content">
              <b>Feedback on Understanding</b>: {{ feedbackContent?.understanding }}
            </div>
          </div>

          <div class="message-container">
            <div class="content">
              <b>Feedback on Initial Ideation</b>: {{ feedbackContent?.initial_ideation }}
            </div>
          </div>

          <div class="message-container">
            <div class="content">
              <b>Feedback on Idea Justification</b>: {{ feedbackContent?.idea_justification }}
            </div>
          </div>

          <div class="message-container">
            <div class="content">
              <b>Feedback on Implementation</b>: {{ feedbackContent?.implementation }}
            </div>
          </div>

          <div class="message-container">
            <div class="content">
              <b>Feedback on Review (Dry Run)</b>: {{ feedbackContent?.review_dry_run }}
            </div>
          </div>

          <div class="message-container">
            <div class="content">
              <b>Feedback on Evaluation</b>: {{ feedbackContent?.evaluation }}
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
  <div v-else>
    <loader></loader>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref, watch, onMounted } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import loader from './misc/loader.vue';

interface ChatMessage {
  content: string;
  role: string;
}

interface FeedbackContent {
  understanding: string;
  initial_ideation: string;
  idea_justification: string;
  implementation: string;
  review_dry_run: string;
  evaluation: string;
}

export default defineComponent({

  components: {
    loader,
  },
  methods: {

  },
  setup(props, context) {

    const backendURL = '/api';
    const transcript = ref<ChatMessage[]>([]); // Store the transcript locally
    const feedbackContent = ref<FeedbackContent>();

    // Fetch transcript from API when the component is mounted
    onMounted(async () => {
      try {
        const sessionID = Cookies.get('sessionID');

        const requestBody = {
          sessionID: sessionID,
        };

        const response = await axios.post(`${backendURL}/retrieveFeedback/general`, requestBody); // Replace with actual API endpoint
        console.log(response)

        transcript.value = response.data['transcript'];

        feedbackContent.value = JSON.parse(response.data['feedback']);

      } catch (error) {
        console.error('Error fetching transcript:', error);
      }
    });

    return {
      transcript,
      feedbackContent,
    };
  },
});
</script>



<style scoped>
.headline {
  text-align: center;
}

.transcript {
  border: 1px solid #ccc;
  background: white;
  max-height: 82vh;
  padding: 1em;
  overflow: auto;
  max-width: 50rem;
  margin: 0 auto 2em auto;
  box-shadow: 2px 2px 5px 2px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1em;
  margin-bottom: 1em;

  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  max-width: 45rem;
  z-index: 2;
  box-sizing: border-box;
  border-radius: 1rem;
}

.message {
  width: 95%;
  border-radius: 10px;
  padding: .5em;
  margin-bottom: .5em;
  margin-top: .5em;
  font-size: .9em;
  text-align: left;
}

.message-in {
  background: #F1F0F0;
  color: black;
}

.highlight {
  background: #ffeca2;
  /* Highlight color */
  /* Add other styles for highlighting */
}

.highlight-seek-time {
  --tw-text-opacity: 1;
  background: rgb(250, 200, 200);
  /* background: var(--tw-bg-opacity, rgba(255, 236, 162, var(--tw-bg-opacity, 1))); Background color from .highlight */
  /* Highlight color */
  /* Add other
   styles for highlighting */
}


.message-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border: 1px solid #ccc;
  /* Add border for the box */
  background-color: #fefefe;
  /* Light background color for the box */
  padding: 10px;
  /* Add padding inside the box */
  border-radius: 8px;
  /* Rounded corners for the box */
  margin-bottom: 10px;
  /* Add space between messages */
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
  /* Add a subtle shadow */
}

.content {
  flex-grow: 1;
}

.speaker-1 {
  color: #368a02;
  /* Text color for Speaker 1 */
}

.speaker-2 {
  color: #0d6efd;
  /* Text color for Speaker 2 */
}

.margin-right {
  margin-right: 25px;
  /* Adjust margin as needed */
}

.margin-left {
  margin-left: 25px;
  /* Adjust margin as needed */
}
</style>