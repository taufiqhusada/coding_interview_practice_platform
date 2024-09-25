<template>
    <div class="row">
        <div class="col-6">
            <div class="chat mt-3">
                <div class="contact">
                    <div class="name">Learn from example</div>
                </div>
                <div id="chat-messages" class="messages" ref="messages">
                    <div v-for="(message, index) in currChatMessages" :key="index">
                        <div :class="message.role === 'interviewee' ? 'message interviewee' : 'message interviewer'"
                            :data-text="message.explanation" class="tooltip-box">
                            <span>{{ message.content }}</span>
                        </div>
                    </div>
                </div>
                <div class="input">
                    <!-- <button @click="generateExample" class="btn btn-primary">Generate Example</button> -->
                    <button @click="getNextInteraction" class="btn btn-primary" style="margin-left: 20px;">Next</button>
                </div>
            </div>

        </div>
        <div class="col-6">
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
            <div class="mt-3">
                <Codemirror placeholder="" :style="{ height: '35vh' }" :autofocus="true" :indent-with-tab="true"
                    style="max-width:40rem; font-size: smaller;" :value="code" :tab-size="2" :extensions="extensions"  v-model="code"/>
            </div>


        </div>


    </div>

</template>


<script setup lang="ts">
import { defineComponent, ref, nextTick, onMounted } from 'vue';
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

const messages =  ref<HTMLDivElement | null>(null);// Create a ref for the chat-messages div



const backendURL = '/api';
const problemStatement = `<b>Intersection of Two Arrays</b>
                          <p>Given two integer arrays <code>nums1</code> and <code>nums2</code>, return an array of their intersection.</p>
                          <p>Each element in the result must appear as many times as it shows in both arrays, and you may return the result in any order.</p>

                          <b>Example 1:</b>
                          <pre><code>Input: nums1 = [1,2,2,1], nums2 = [2,2]\nOutput: [2,2]</code></pre>

                          <b>Example 2:</b>
                          <pre><code>Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]\nOutput: [4,9]</code></pre>
                          <p>Note: [9,4] is also accepted.</p>`;

const generateExample = async () => {
    const requestBody = {
        messages: '',
    };

    try {
        const response = await axios.post(`${backendURL}/generateSimulation`, requestBody);
        allChatMessages.value.pop();
        if (response.status === 200) {
            // Update the feedback field with the response from GPT-4
            allChatMessages.value = response.data;
        } else {
            console.error('Failed to get chat from GPT:', response.status, response.data);
        }
    } catch (error) {
        console.error('Error while chatting with GPT:', error);
    }
};

onMounted(async () => {
    await generateExample(); // Wait for the example to be generated
});

const getNextInteraction = async () => {
    const nextMessage = allChatMessages.value[currentIdxChat.value];
    if (nextMessage) {
        currChatMessages.value.push({
            content: nextMessage.content,
            role: nextMessage.role,
            explanation: nextMessage.explanation,
            code: nextMessage.code,
        });

        scrollToBottom();


        // If there is code, simulate typing it
        if (nextMessage.code !== "") {
            await typeCode(nextMessage.code); 
        }
        currentIdxChat.value++;
    }
};


const typeCode = (codeContent: string) => {
    return new Promise((resolve) => {
        const typingSpeed = 50; // Typing speed in milliseconds
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
    height: 80vh;
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
</style>