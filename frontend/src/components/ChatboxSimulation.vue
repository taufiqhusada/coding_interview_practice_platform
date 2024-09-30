<template>
    <div class="problemBox mt-3">
        <div class="contact">
            <h6>Problem Description</h6>
        </div>
        <div class="problemStatement" ref="problemBox">
            <div class="container mt-2">
                <span v-html="problemStatement"></span>
            </div>
        </div>
    </div>

    <div class="d-flex align-items-center mt-3">
        <button v-if="!isRecording && !isSendingMessage" @click="startRecording" class="btn btn-primary"
            style="margin-right: 20px; width: auto; min-width: 150px; white-space: nowrap;">
            Start Session
        </button>
        <button v-if="isRecording" @click="stopRecording" class="btn btn-outline-danger"
            style="margin-right: 20px; width: auto; min-width: 150px; white-space: nowrap;">
            Stop Session
        </button>

        <button v-if="isRecording" @click="toggleTranscript" class="btn btn-outline-primary"
            style="margin-right: 20px; width: auto; min-width: 150px; white-space: nowrap;">
            {{ isTranscriptVisible ? 'Hide Transcript' : 'Show Transcript' }}
        </button>

        <button v-if="isRecording && !isSendingMessage" @click="getResponseFromGPT" class="btn btn-outline-primary"
            style="margin-right: 20px; width: auto; min-width: 150px; white-space: nowrap;">
            Get Response
        </button>

        <div v-if="isSendingMessage">
            <loaderSimple style="margin-left: 20px; margin-right: 40px"></loaderSimple>
        </div>

        <div class="form-group mb-0" style="flex-grow: 1;"> <!-- Use flex-grow for better responsiveness -->
            <select id="interactionMode" class="form-select" style="padding: 0.375rem 0.75rem; min-width: 150px;" @change="changeInteractionMode" v-model="selectedInteractionMode">
                <option value="manualReply">Manual Reply</option>
                <option value="autoReplay">Auto Reply</option>
            </select>
        </div>
    </div>


    <div v-if="isTranscriptVisible && isRecording" class="chat mt-3">
        <div class="contact">
            <div class="name">Live Transcript</div>
        </div>

        <!-- Conditionally render the transcript -->
        <div id="chat-messages" class="messages" ref="messages">
            <div v-for="(message, index) in chatMessages" :key="index">
                <div :class="message.role === 'interviewee' ? 'message interviewee' : 'message interviewer'">
                    <div v-if="message.isTyping" class="typing">
                        <div class="dot dot-1"></div>
                        <div class="dot dot-2"></div>
                        <div class="dot dot-3"></div>
                    </div>
                    <div v-else>
                        <span v-html="message.content"></span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Other existing content (e.g., recording button) -->
        <div class="d-flex flex-row m-2">
            <!-- <div class="form-group" style="width: 100%;">
                <select id="languageSelect" class="form-select">
                    <option value="active">Active</option>
                    <option value="passive">Passive</option>
                    <option value="random">Random</option>
                </select>
            </div> -->
            <div class="input" style="width: 200px;">

            </div>
        </div>
    </div>
</template>


<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios from 'axios';
import io, { Socket } from 'socket.io-client';
import { throws } from 'assert';
import Cookies from 'js-cookie';
import router from '@/router';
import loaderSimple from './misc/loader_simple.vue';



interface Metadata {
    [key: string]: string; // Or whatever type your values are
}

interface ChatMessage {
    content: string;
    role: 'interviewee' | 'interviewer';
    isTyping?: boolean;
}

interface ChatMessageBackend {
    content: string;
    role: 'user' | 'assistant';
}


const PracticeState = {
  NotStarted: -1,
  Practicing: 0,
  FeedbackReceived: 1
}


export default defineComponent({
    props: {
        code: {
            type: String,
            required: false
        }
    },
    components: {
        loaderSimple,
    },
    data() {
        return {
            chatMessages: [] as ChatMessage[], // Define the type for chatMessages
            backendURL: '/api',
            isRecording: false,
            recognition: null as SpeechRecognition | null,
            ws: null as Socket | null,
            problemStatement: `<b>Intersection of Two Arrays</b>
                                <p>Given two integer arrays <code>nums1</code> and <code>nums2</code>, return an array of their intersection.</p>
                                <p>Each element in the result must appear as many times as it shows in both arrays, and you may return the result in any order.</p>

                                <b>Example 1:</b>
                                <pre><code>Input: nums1 = [1,2,2,1], nums2 = [2,2]\nOutput: [2,2]</code></pre>

                                <b>Example 2:</b>
                                <pre><code>Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]\nOutput: [4,9]</code></pre>`,
            silenceTimer: undefined as ReturnType<typeof setTimeout> | undefined,
            isSendingMessage: false,
            isTranscriptVisible: true,
            isManualModeReply: true,
            selectedInteractionMode: "manualReply",
            interimTranscript: '',
            currentTranscript: '',
        };
    },

    methods: {
        toggleTranscript() {
            this.isTranscriptVisible = !this.isTranscriptVisible;
        },
        // Define the keydown handler
        handleKeydown(event: KeyboardEvent) {
            // Check if Ctrl+Space (Windows/Linux) or Cmd+Space (Mac) is pressed
            if (this.isManualModeReply && (event.ctrlKey || event.metaKey) && event.code === 'KeyM') {
                console.log("button pressed")
                event.preventDefault(); // Prevent the default browser behavior
                this.getResponseFromGPT(); // Call the method
            }
        },

        startRecording() {
            this.isRecording = true;

            // Initialize the Socket.IO connection
            this.ws = io('http://127.0.0.1:5000/ws');
            // When the connection is established
            this.ws.on('connect', () => {
                console.log("Connected to server");
                this.isSendingMessage = true;
                this.startRecognition();
                this.recognition?.stop();
                this.chatMessages.push({ role: "interviewer", content: "loading", isTyping: true });
                this.ws?.send({ 'is_first': true });
            });

            // Listen for messages from the server
            this.ws.on('message', (data: any) => {
                console.log(data);
                this.processResponse(data);
            });

            // Handle connection errors
            this.ws.on('connect_error', (error: any) => {
                console.error('Socket.IO connection error:', error);
            });

            // Handle disconnection
            this.ws.on('disconnect', () => {
                if (this.recognition) {
                    this.recognition.stop();
                }
                console.log('Socket.IO disconnected.');
            });

            console.log('try to emit')

            // emit to parent
            this.$emit('update:PracticeState', PracticeState.Practicing); 
        },

        processResponse(res: any) {

            const ttsResponseData = res['audio_data'];
            const gptResponseText = res['text_response'];

            this.recognition?.stop(); // I don't know if this is necessary

            const audioContext = new AudioContext();

            const audioData = atob(ttsResponseData);

            // Convert the audio data to an ArrayBuffer
            const audioBuffer = new ArrayBuffer(audioData.length);
            const audioView = new Uint8Array(audioBuffer);
            for (let i = 0; i < audioData.length; i++) {
                audioView[i] = audioData.charCodeAt(i);
            }

            const audioBlob = new Blob([audioView], { type: 'audio/mp3' });

            // Decode the ArrayBuffer into audio data
            audioContext.decodeAudioData(audioBuffer, (decodedBuffer) => {
                const source = audioContext.createBufferSource();
                source.buffer = decodedBuffer;
                source.connect(audioContext.destination);

                source.onended = () => {
                    this.isSendingMessage = false;
                    // Audio has ended, add your logic here
                    this.recognition?.start();

                };

                this.chatMessages.pop();
                this.chatMessages.push({ role: "interviewer", content: gptResponseText });
                this.scrollToBottom();

                source.start();

            });
        },

        startRecognition() {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = true;
            this.recognition.interimResults = true;

            this.currentTranscript = '';

            this.recognition.onstart = () => {
                console.log('Speech recognition is on. Speak into the microphone.');
            };

            this.recognition.onresult = (event) => {
                // Clear any existing silence timer
                if (this.silenceTimer) {
                    clearTimeout(this.silenceTimer);
                }

                this.interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        this.currentTranscript += event.results[i][0].transcript;
                    } else {
                        this.interimTranscript += event.results[i][0].transcript;
                    }
                }

                if (this.isManualModeReply) { // manual mode reply
                    // Add or update the user's message
                    


                } else {
                    console.log('auto')
                    // Set a new silence timer
                    this.silenceTimer = setTimeout(() => {
                        if (this.ws && this.currentTranscript.trim() !== '') {
                            // Add or update the user's message
                            if (this.chatMessages.length > 0 && this.chatMessages[this.chatMessages.length - 1].role === "interviewee") {
                                this.chatMessages[this.chatMessages.length - 1] = { role: "interviewee", content: this.currentTranscript + this.interimTranscript };
                            } else {
                                return
                            }
                            this.scrollToBottom();

                            this.isSendingMessage = true;
                            this.recognition?.stop();

                            this.chatMessages.push({ role: "interviewer", content: "loading", isTyping: true });

                            console.log("Silence detected, sending message");
                            this.ws.send({ 'messages': this.chatMessages, 'code': this.code, 'is_first': false });
                            this.scrollToBottom();
                            this.currentTranscript = '';
                        }
                    }, 2000);
                }

            };

            this.recognition.onerror = (event) => {
                console.log('Speech recognition error: ' + event.error);
            };

            this.recognition.onspeechstart = (e) => {
                console.log("restarted")
                clearTimeout(this.silenceTimer);
                this.chatMessages.push({ role: "interviewee", content: "loading", isTyping: true });
                this.scrollToBottom();
            }

            // this.recognition.onend = () => {
            //     if (!this.isSendingMessage) {
            //         this.recognition?.start();
            //     }
            // };

            this.recognition.start();
        },

        async stopRecording() {
            this.isSendingMessage = true; // just to set the flag
            this.recognition?.stop();
            this.isRecording = false;
            this.ws?.disconnect();

            // save 
            try {
                // Make a POST request to your API
                const requestBody = {
                    transcript: this.chatMessages,
                };
                const response = await axios.post(`${this.backendURL}/getFeedback/general`, requestBody);
                if (response.status === 200) {
                    // Update the feedback field with the response from GPT-4
                    console.log(response.data)

                    const sessionId = response.data["session_id"];
                    const feedback = response.data["feedback"]

                    console.log(sessionId)
                    console.log(feedback)

                    Cookies.set('sessionID', sessionId, { expires: 120 / (24 * 60) });
                    router.push('/feedback');

                } else {
                    // Handle API response error
                    console.error('Failed to save and get feedback', response.status, response.data);
                    this.scrollToBottom();
                }
            } catch (error) {
                // Handle network or other errors
                console.error('Error while saving and get feedback', error);
            }
        },

        mapChatMessagesToBackendFormat(chatMessages: ChatMessage[], isInterviewerTurn: Boolean) {
            let assistant = 'interviewer'
            if (!isInterviewerTurn) {
                assistant = 'interviewee'
            }


            const chatMessagesWithoutTyping = chatMessages.map(({ isTyping, ...rest }) => ({
                content: rest.content,
                role: rest.role === assistant ? 'assistant' : 'user',
            }));

            return chatMessagesWithoutTyping;
        },

        scrollToBottom() {
            const messagesContainer = this.$refs.messages as HTMLElement;
            if (messagesContainer) {
                this.$nextTick(() => {
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                });
            }
        },

        getResponseFromGPT() {
            if (this.chatMessages.length > 0 && this.chatMessages[this.chatMessages.length - 1].role === "interviewee") {
                this.chatMessages[this.chatMessages.length - 1] = { role: "interviewee", content: this.currentTranscript + this.interimTranscript };
            } 
            this.scrollToBottom();
            this.currentTranscript = '';

            this.isSendingMessage = true;
            this.recognition?.stop();

            this.chatMessages.push({ role: "interviewer", content: "loading", isTyping: true });

            console.log("Silence detected, sending message");
            this.ws?.send({ 'messages': this.chatMessages, 'code': this.code, 'is_first': false });
            this.scrollToBottom();
        },

        changeInteractionMode() {
            if (this.selectedInteractionMode == "manualReply") {
                this.isManualModeReply = true;
            } else {
                this.isManualModeReply = false;
            }
            console.log(this.isManualModeReply)
        },

        getTranscriptSession(): ChatMessage[] {
            return this.chatMessages;
        },

        clearTranscriptSession(idxStart: number){
            this.chatMessages = this.chatMessages.slice(idxStart);
        }
    },

    mounted() {
        console.log("mounted")
        // Bind the event on component mount
        window.addEventListener('keydown', (event) => this.handleKeydown(event));
    },
    beforeUnmount() {
        // Unbind the event on component unmount
        window.removeEventListener('keydown', this.handleKeydown);
    },

    watch: {

    },
});
</script>

<style scoped>
.contact {
    position: relative;
    padding-left: 1rem;
    height: 3rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.name {
    font-weight: 500;
    margin-bottom: 0.125rem;
}

.problemBox {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    max-width: 100%;
    height: 40vh;
    z-index: 2;
    box-sizing: border-box;
    border-radius: 1rem;
    background: white;
    box-shadow: 2px 2px 5px 2px rgba(0, 0, 0, 0.3);
}

.chat {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    max-width: 100%;
    height: 40vh;
    z-index: 2;
    box-sizing: border-box;
    border-radius: 1rem;
    background: white;
    box-shadow: 2px 2px 5px 2px rgba(0, 0, 0, 0.3);
}

.messages {
    /* padding: 6rem; */
    background: #F7F7F7;
    /* You can update the background color as needed */
    flex-shrink: 10;
    overflow-y: auto;
    height: 50rem;
    box-shadow:
        inset 0 2rem 2rem -2rem rgba(0, 0, 0, 0.05),
        inset 0 -2rem 2rem -2rem rgba(0, 0, 0, 0.05);
}

.problemStatement {
    /* padding: 6rem; */
    background: white;
    /* You can update the background color as needed */
    flex-shrink: 10;
    overflow-y: auto;
    height: 50rem;
    box-shadow:
        inset 0 2rem 2rem -2rem rgba(0, 0, 0, 0.05),
        inset 0 -2rem 2rem -2rem rgba(0, 0, 0, 0.05);
}

.message {
    box-sizing: border-box;
    padding: 0.5rem 2rem;
    margin: 1rem;
    background: #FFF;
    min-height: 2.25rem;
    width: fit-content;
    max-width: 66%;
    box-shadow:
        0 0 2rem rgba(0, 0, 0, 0.075),
        0rem 1rem 1rem -1rem rgba(0, 0, 0, 0.1);
}

.message.interviewer {
    /* margin: 1rem 1rem 1rem auto; */
    /* border-radius: 1.125rem 1.125rem 0 1.125rem; */
    border-radius: 1.125rem 1.125rem 0 1.125rem;

    background: #333;
    /* You can update the color as needed */
    color: white;
}

.message.interviewee {
    margin: 1rem 1rem 1rem auto;
    border-radius: 1.125rem 1.125rem 1.125rem 0;

}

.typing {
    display: flex;
    align-items: center;
}

.dot {
    width: 8px;
    height: 8px;
    background-color: #555;
    border-radius: 50%;
    margin: 0 4px;
    animation: bounce 1s infinite;
}

.dot-1 {
    animation-delay: 0s;
}

.dot-2 {
    animation-delay: 0.2s;
}

.dot-3 {
    animation-delay: 0.4s;
}

@keyframes bounce {

    0%,
    80%,
    100% {
        transform: translateY(0);
    }

    40% {
        transform: translateY(-10px);
    }
}

.input {
    box-sizing: border-box;
    flex-basis: 4rem;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    padding: 0 0.5rem 0 1.5rem;
}

i {
    font-size: 1.5rem;
    margin-right: 1rem;
    color: #666;
    /* You can update the color as needed */
    cursor: pointer;
    transition: color 200ms;
}

i:hover {
    color: #333;
    /* You can update the color as needed */
}

input {
    border: none;
    background-image: none;
    background-color: white;
    padding: 0.5rem 1rem;
    margin-right: 1rem;
    border-radius: 1.125rem;
    flex-grow: 2;
    box-shadow: 2px 2px 5px 2px rgba(0, 0, 0, 0.3);
}

input::placeholder {
    color: #999;
    /* You can update the color as needed */
}

.chat {
    opacity: 1;
    transition: opacity 1s;
    /* Adjust the transition duration as needed */
}

.show-chatbox .chat {
    opacity: 0;
}

.recording {
    color: red;
    /* Change the color to red when recording */
    animation: pulse 1s infinite;
    /* Add a pulsating animation */
}

@keyframes pulse {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.1);
    }

    100% {
        transform: scale(1);
    }
}

/* Custom styles for the dropdown */
.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown-button {
    background-color: #6c757d;
    color: #fff;
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.dropdown-menu {
    display: none;
    position: absolute;
    background-color: #fff;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 1;
    min-width: 160px;
}

.dropdown-item {
    padding: 8px 12px;
    text-decoration: none;
    display: block;
    color: #333;
}

.dropdown-item:hover {
    background-color: #f8f9fa;
}

.dropdown:hover .dropdown-menu {
    display: block;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

/* Apply the animation to the chatbox */
.message {
    animation: fadeIn 0.5s ease-in-out;
}

.input-group {
    display: flex;
    align-items: center;
}

.time-input {
    flex-grow: 1;
    border: none;
    /* Remove input border */
}

.input-group-btn {
    padding: 0;
    /* Remove padding */

    border: none;
    background-image: none;
    padding: 0.1rem;
    border-radius: 1.125rem;
    box-shadow: 1px 2px 5px 1px rgba(0, 0, 0, 0.3);
}

.pin-button {
    padding: 0.375rem 0.75rem;
    margin-right: -1px;
    border-top-left-radius: 1.125rem;
    border-bottom-left-radius: 1.125rem;
}

.pin-button-clicked {
    background-color: #ffeca2;
}

.pin-button:hover {
    background-color: #e2e6ea;
    /* Slightly different background on hover/focus for feedback */
}

.pin-icon {
    width: 16px;
    /* Or any other size */
    height: auto;
}

.message a {
    text-decoration: underline;
    color: blue;
}

.refresh-container {
    display: flex;
    /* This turns the container into a flex container */
    align-items: center;
    /* This vertically centers the children */
    gap: 10px;
    /* This adds some space between the children */
}
</style>