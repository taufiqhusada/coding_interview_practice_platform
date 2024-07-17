
import axios from 'axios';
import fs from 'fs';

export interface Subtitle {
    number: string;
    startTime: number;
    endTime: number;
    text: string;
}

export default class GPTService {
    async getTranscriptFromWhisper(audioBlob: Blob) {
        try {
            // Replace 'YOUR_WHISPER_API_KEY' and 'YOUR_WHISPER_API_ENDPOINT' with your actual API key and endpoint
            const backendURL = '/api';
            const apiURL = `${backendURL}/simulation/transcript`

            // Create a FormData object to send the audio file
            const formData = new FormData();
            // Convert the Blob to a File object with the desired filename and type
            const audioFile = new File([audioBlob], 'audio.webm', { type: 'audio/webm' });

            console.log(audioFile, audioFile.name)
            // Append the audio file to the FormData object
            formData.append('file', audioFile, audioFile.name);

            // Make an HTTP POST request to the Whisper API
            const response = await axios.post(apiURL, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            console.log(response);

            // Extract the transcript from the response
            const transcript = response.data.data as Subtitle[];

            return transcript

        } catch (error) {
            console.error('Error getting transcript from Whisper API:', error);
            return [];
        }
    };

    async generateGptResponse(transcript: Array<{ text: string, timeOffset: number, speaker: string }>, instruction: string) {
        try {

            const backendURL = '/api';
            const apiURL = `${backendURL}/simulation/response`

            // Define the request payload following the cURL example
            const requestData = {
                model: 'gpt-3.5-turbo',
                transcript: transcript,
                instruction: instruction,
            };

            console.log(requestData)

            // Send the request to the OpenAI API
            const gptResponse = await axios.post(apiURL, requestData);

            console.log(gptResponse)
            return gptResponse.data;
        } catch (error) {
            console.error('Error generating GPT response:', error);
            return '';
        }
    };

}