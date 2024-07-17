import axios from 'axios';


export async function postInterviewData(data: {
    sessionID: string;
    username_interviewer: string;
    username_interviewee: string;
    transcript_link: string;
    video_link: string;
  }) {

    let backendURL = '/api'

    const apiUrl = `${backendURL}/interviews`; // Replace with your API URL
  
    try {
      const response = await axios.post(apiUrl, data);
  
      if (response.status === 200) {
        console.log('interveiw data saved successfully:', response.data);
        return response.data
      } else {
        console.error('Failed to send data:', response.status, response.data);
      }
    } catch (error) {
      console.error('Error while sending data:', error);
    }
  }


export async function postInterviewTranscriptData(data: {
    sessionID: string;
    transcript: any,
    identifiedMoments: any[];
  }): Promise<void> {

    let backendURL = '/api'

    const apiUrl = `${backendURL}/interviews/transcript`; // Replace with your API URL
  
    try {
      const response = await axios.post(apiUrl, data);
  
      if (response.status === 200) {
        console.log('transcript data saved successfully:', response.data);
      } else {
        console.error('Failed to send data:', response.status, response.data);
      }
    } catch (error) {
      console.error('Error while sending data:', error);
    }
  }

export async function getAllData(token: string) {
  let backendURL = '/api';
  const apiUrl = `${backendURL}/retrieve`;

  try {
    const response = await axios.get(apiUrl, {
      headers: {
        Authorization: `Bearer ${token}` // Set the Authorization header with Bearer token
      }
    });
    console.log(response);

    if (response.status === 200) {
      return response.data;
    } else {
      console.error('Failed to send data:', response.status, response.data);
    }
  } catch (error) {
    console.error('Error while sending data:', error);
  }
}