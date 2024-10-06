<template>
    <div class="row">
        <div class="col-6">
            <div class="icon-container mt-3">
                <!-- Floating Icon -->
                <div class="floating-icon" @click="togglePopup">
                    <i class="fas fa-comments"></i>
                </div>
                <div v-if="showPopup" class="popup-message">
                    <p>{{ popupMessage }}</p>
                </div>
            </div>
            <div class="chat mt-3">
                <div class="contact">
                    <div class="name">Learn from example</div>
                </div>
                <div id="chat-messages" class="messages" ref="messages">
                    <div v-for="(message, index) in currChatMessages" :key="index">
                        <div :class="[
                    'message',
                    message.role === 'interviewee' ? 'interviewee' : 'interviewer',
                    message.explanation !== '' ? 'tooltip-top' : ''
                ]" v-if="message.explanation !== ''" :data-tooltip="message.explanation">
                            <span>{{ message.content }}</span>
                        </div>
                        <!-- If no explanation, render without tooltip -->
                        <div :class="['message', message.role === 'interviewee' ? 'interviewee' : 'interviewer']"
                            v-else>
                            <span>{{ message.content }}</span>
                        </div>
                    </div>
                </div>
                <div class="input">
                    <button v-if="isPaused" @click="continueInteraction" class="btn btn-primary" style="">Continue</button>
                    <div v-else>
                         <!-- <button @click="generateExample" class="btn btn-primary">Generate Example</button> -->
                        <button @click="pauseInteraction" class="btn btn-outline-primary" style="">Pause</button>
                        <button @click="getNextInteraction" class="btn btn-primary" style="margin-left: 20px;">Next</button>
                    </div>
                   

                </div>
            </div>

        </div>
        <div class="col-6">
            <div class="problemBox mt-3 container">
                <div class="d-flex justify-content-between align-items-center mt-2">
                    <h6>Problem Description</h6>
                    <div class="problem-select">
                        <select class="form-select" style="min-width: 200px;" v-model="problemNumber" :disabled="isExampleFetched">
                            <!-- <option selected>Select Problem</option> -->
                            <option value="0">Problem 1</option>
                            <option value="1">Problem 2</option>
                            <option value="2">Problem 3</option>
                            <option value="3">Problem 4</option>
                        </select>
                    </div>
                </div>
                <div class="problemStatement" ref="problemBox">
                    <div class="container mt-2">
                        <span v-html="problemStatement"></span>
                    </div>
                </div>
            </div>
            <div class="mt-3">
                <Codemirror placeholder="" :style="{ height: '35vh' }" :autofocus="true" :indent-with-tab="true"
                    style="max-width:40rem; font-size: smaller;" :value="code" :tab-size="2" :extensions="extensions"
                    v-model="code" />
            </div>


        </div>


    </div>

</template>


<script setup lang="ts">
import { defineComponent, ref, nextTick, onMounted, watch } from 'vue';
import axios from 'axios';
import { Codemirror } from 'vue-codemirror'
import { javascript } from '@codemirror/lang-javascript'
import { python } from '@codemirror/lang-python'
import { java } from '@codemirror/lang-java'
import { cpp } from '@codemirror/lang-cpp'
import { oneDark } from '@codemirror/theme-one-dark'
import { EditorState } from "@codemirror/state"
import { EditorView } from "@codemirror/view"


interface Metadata {
    [key: string]: string; // Or whatever type your values are
}

interface ChatMessage {
    content: string;
    role: 'interviewee' | 'interviewer';
    explanation: string;
    code: string;
    audio_base64: string;
}

interface ChatMessageBackend {
    content: string;
    role: 'user' | 'assistant';
}

type ReferenceDocs = {
    content: string;
    metadata: Metadata;
    source: string;
    type: string;
};


const code = ref("")
const selectedLanguage = ref('python')
const extensions = ref([python(), oneDark, EditorView.editable.of(false)])

const currentIdxChat = ref(0)

const allChatMessages = ref<ChatMessage[]>([]);  // Using ref for reactivity
const currChatMessages = ref<ChatMessage[]>([]);  // Using ref for reactivity

const messages = ref<HTMLDivElement | null>(null);// Create a ref for the chat-messages div

const showPopup = ref(true) // Control popup visibility
const popupMessage = ref("Ready to learn? Click the start button to see the example think-aloud process")

const isPaused = ref(false)

let currentAudioSource: AudioBufferSourceNode;

const isExampleFetched = ref(false)

const problemNumber = ref(0);
const problemList = ref([
    `<b>Intersection of Two Arrays</b>
        <p>Given two integer arrays <code>nums1</code> and <code>nums2</code>, return an array of their intersection.</p>
        <p>Each element in the result must appear as many times as it shows in both arrays, and you may return the result in any order.</p>
        <b>Example 1:</b>
        <pre><code>Input: nums1 = [1,2,2,1], nums2 = [2,2]\nOutput: [2,2]</code></pre>
        <b>Example 2:</b>
        <pre><code>Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]\nOutput: [4,9]</code></pre>`,
    `<b>Two Sum</b>
        <p>Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.</p>
        <p>You may assume that each input would have exactly one solution, and you may not use the same element twice.</p>`,
    'Problem 3: Description goes here.',
    'Problem 4: Description goes here.'
]);

const problemStatement = ref(problemList.value[0]);

const backendURL = '/api';

watch(problemNumber, (newProblemNumber) => {
    problemStatement.value = problemList.value[newProblemNumber];
    console.log(`Problem changed to ${newProblemNumber}:`, problemStatement.value);
});

const generateExample = async (problemNumber: number) => {
    const requestBody = {
        messages: '',
        problem_index: problemNumber
    };

    try {
        const response = await axios.post(`${backendURL}/generateSimulation`, requestBody);
        allChatMessages.value.pop();
        if (response.status === 200) {
            // Update the feedback field with the response from GPT-4
            allChatMessages.value = response.data;
            isExampleFetched.value = true;
        } else {
            console.error('Failed to get chat from GPT:', response.status, response.data);
        }
    } catch (error) {
        console.error('Error while chatting with GPT:', error);
    }
};

onMounted(async () => {
    // await generateExample(); // Wait for the example to be generated
});

const getNextInteraction = async () => {
    if (!isExampleFetched.value){
        await generateExample(problemNumber.value); 
    }

    if (isPaused.value){
        return;
    }

    const nextMessage = allChatMessages.value[currentIdxChat.value];
    if (nextMessage) {
        currChatMessages.value.push({
            content: nextMessage.content,
            role: nextMessage.role,
            explanation: nextMessage.explanation,
            code: nextMessage.code,
            audio_base64: "",
        });

        if (nextMessage.explanation==null || nextMessage.explanation == "" || nextMessage.role == 'interviewer'){
            showPopup.value = false;
        } else {
            showPopup.value = true;
            popupMessage.value = nextMessage.explanation;
        }

        scrollToBottom();

        processAudio(nextMessage);
        currentIdxChat.value++;
    }
};


const pauseInteraction = async () => {
    if (currentAudioSource) {
        currentAudioSource.stop(); // Stop the previous audio source
    }

    isPaused.value= true;
}

const continueInteraction = async () => {
    isPaused.value= false;
    getNextInteraction();
}

const typeCode = (codeContent: string) => {
    return new Promise((resolve) => {
        const typingSpeed = 150; // Typing speed in milliseconds
        const lines = codeContent.split("\n"); // Split code into lines
        let currentLine = 0;
        let currentChar = 0;

        const typeInterval = setInterval(() => {
            if (currentLine < lines.length) {
                if (currentChar < lines[currentLine].length) {
                    code.value += lines[currentLine].charAt(currentChar);
                    currentChar++;
                } else {
                    code.value += "\n"; // Move to the next line
                    currentLine++;
                    currentChar = 0; // Reset char index for the new line
                }
            } else {
                clearInterval(typeInterval);
                resolve(null); // Resolve the promise when done
            }
        }, typingSpeed);
    });
};

// Function to scroll to the bottom of the chat messages container
const scrollToBottom = () => {
    if (messages.value) {
        nextTick(() => {
            if (messages.value)
                messages.value.scrollTop = messages.value.scrollHeight;
        });
    }
};

const processAudio = async (res: any) => {  
    if (currentAudioSource) {
        currentAudioSource.stop(); // Stop the previous audio source
    }

    // If there is code, simulate typing it
    let typeCodePromise: Promise<any> = Promise.resolve(); 
    if (res.code && res.code !== "") {
        console.log("not empty code", res.code)
        typeCodePromise = typeCode(res.code);
    }

    const ttsResponseData = res['audio_base64'];

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
        currentAudioSource = audioContext.createBufferSource();
        currentAudioSource.buffer = decodedBuffer;
        currentAudioSource.connect(audioContext.destination);

        currentAudioSource.onended = async () => {
            // Audio has ended, add your logic here
            await typeCodePromise;
            // Set a 2-second delay before calling getNextInteraction
            setTimeout(() => {
                getNextInteraction();
            }, 2000);  // 2000 ms = 2 seconds

        };

        currentAudioSource.start();

    });
};

const togglePopup = () => {
    showPopup.value = !showPopup.value
    // Auto-hide popup after 3 seconds
    // if (showPopup.value) {
    //   setTimeout(() => {
    //     showPopup.value = false
    //   }, 3000)
    // }
};

</script>


<style scoped>
.contact {
    position: relative;
    padding-left: 2rem;
    height: 3rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.name {
    font-weight: 500;
    margin-bottom: 0.125rem;
}

.chat {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    max-width: 100%;
    height: 75vh;
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
    z-index: 1;
    flex-shrink: 10;
    overflow-x: visible;
    overflow-y: scroll;
    position: relative;
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
    overflow: visible;
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

.problemBox {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    max-width: 100%;
    height: 45vh;
    z-index: 2;
    box-sizing: border-box;
    border-radius: 1rem;
    background: white;
    box-shadow: 2px 2px 5px 2px rgba(0, 0, 0, 0.3);
}


/**
 * Tooltip Styles
 */

/* Base styles for the element that has a tooltip */
[data-tooltip],
.tooltip {
    position: relative;
    cursor: pointer;
}

/* Base styles for the entire tooltip */
[data-tooltip]:before,
[data-tooltip]:after,
.tooltip:before,
.tooltip:after {
    position: absolute;
    visibility: hidden;
    -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=0)";
    filter: progid:DXImageTransform.Microsoft.Alpha(Opacity=0);
    opacity: 0;
    -webkit-transition:
        opacity 0.2s ease-in-out,
        visibility 0.2s ease-in-out,
        -webkit-transform 0.2s cubic-bezier(0.71, 1.7, 0.77, 1.24);
    -moz-transition:
        opacity 0.2s ease-in-out,
        visibility 0.2s ease-in-out,
        -moz-transform 0.2s cubic-bezier(0.71, 1.7, 0.77, 1.24);
    transition:
        opacity 0.2s ease-in-out,
        visibility 0.2s ease-in-out,
        transform 0.2s cubic-bezier(0.71, 1.7, 0.77, 1.24);
    -webkit-transform: translate3d(0, 0, 0);
    -moz-transform: translate3d(0, 0, 0);
    transform: translate3d(0, 0, 0);
    pointer-events: none;
}

/* Show the entire tooltip on hover and focus */
[data-tooltip]:hover:before,
[data-tooltip]:hover:after,
[data-tooltip]:focus:before,
[data-tooltip]:focus:after,
.tooltip:hover:before,
.tooltip:hover:after,
.tooltip:focus:before,
.tooltip:focus:after {
    visibility: visible;
    -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=100)";
    filter: progid:DXImageTransform.Microsoft.Alpha(Opacity=100);
    opacity: 1;
}

/* Base styles for the tooltip's directional arrow */
.tooltip:before,
[data-tooltip]:before {
    z-index: 1001;
    border: 6px solid transparent;
    background: transparent;
    content: "";
}

/* Base styles for the tooltip's content area */
.tooltip:after,
[data-tooltip]:after {
    z-index: 1000;
    padding: 8px;
    width: 160px;
    background-color: #000;
    background-color: hsla(0, 0%, 20%, 0.9);
    color: #fff;
    content: attr(data-tooltip);
    font-size: 14px;
    line-height: 1.2;
}

/* Directions */

/* Top (default) */
[data-tooltip]:before,
[data-tooltip]:after,
.tooltip:before,
.tooltip:after,
.tooltip-top:before,
.tooltip-top:after {
    bottom: 100%;
    left: 50%;
}

[data-tooltip]:before,
.tooltip:before,
.tooltip-top:before {
    margin-left: -6px;
    margin-bottom: -12px;
    border-top-color: #000;
    border-top-color: hsla(0, 0%, 20%, 0.9);
}

/* Horizontally align top/bottom tooltips */
[data-tooltip]:after,
.tooltip:after,
.tooltip-top:after {
    margin-left: -80px;
}

[data-tooltip]:hover:before,
[data-tooltip]:hover:after,
[data-tooltip]:focus:before,
[data-tooltip]:focus:after,
.tooltip:hover:before,
.tooltip:hover:after,
.tooltip:focus:before,
.tooltip:focus:after,
.tooltip-top:hover:before,
.tooltip-top:hover:after,
.tooltip-top:focus:before,
.tooltip-top:focus:after {
    -webkit-transform: translateY(-12px);
    -moz-transform: translateY(-12px);
    transform: translateY(-12px);
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

.problemStatement {
    display: flex;
    flex-direction: column; /* Ensure elements are stacked vertically */
    justify-content: flex-start; /* Align items to the top */
    height: 45vh; /* Set a fixed height */
    overflow: auto; /* Handle overflow if the content is too large */
}
</style>