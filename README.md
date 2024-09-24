# How to: Streaming

Table of Contents

- [Verktøy](#verktøy)
- [Første strøm](#første-strøm)
- [Protokoller](#streaming-protokoller)
  - [RTMP](#rtmp)
  - [RTSP](#rtsp)
  - [SRT](#srt)
  - [HLS](#hls-http-live-streaming)
  - [WebRTC](#webrtc-web-real-time-communication)
- [Nettverk](#nettverk)
  - [TCP](#tcp-transmission-control-protocol)
  - [UDP](#udp-user-datagram-protocol)
  - [Sammenligning](#comparison-of-tcp-and-udp-in-streaming)
- [Kodek](#kodek)
  - [H.264](#h264-advanced-video-coding-or-avc)
  - [H.265](#h265-hevc--high-efficiency-video-coding)
  - [Sammenligning](#comparison-between-h264-and-h265)
- [Transcoding](#transcoding)
- [Optimalisering](#optimizing-video-for-low-bandwidth-usage)

## Verktøy

- ffmpeg: https://community.chocolatey.org/packages/ffmpeg
- gstreamer?: https://community.chocolatey.org/packages/gstreamer
- MediaMTX: https://github.com/bluenviron/mediamtx
- MQTT: https://mqtt.org/
- Eyevinn: https://github.com/Eyevinn/streaming-onboarding
- Kamerakartet: https://www.kamerakartet.no/
  - https://polarislive-lh.akamaized.net/hls/live/2039440/fvn/jcp1YQkJV7Zb4khPH2q8O/master.m3u8
  - https://polarislive-lh.akamaized.net/hls/live/2039440/fvn/hzDaPl9KkIbkcZFUvWFfg/master.m3u8

## Første strøm

``` bash
# Start stream
ffmpeg -re -f lavfi -i testsrc2=rate=25:size=1280x720 -pix_fmt yuv420p -codec:v libx264 -b:v 2048k -preset:v ultrafast -f flv rtmp://example.com:1935/live/demo

# Youtube example
#ffmpeg -i https://polarislive-lh.akamaized.net/hls/live/2039440/fvn/hzDaPl9KkIbkcZFUvWFfg/master.m3u8 -vf scale=256:144 -r 1 -b:v 6k -minrate 6k -maxrate 6k -bufsize 3k -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f flv rtmp://a.rtmp.youtube.com/live2/0g56-0y5z-0jsf-kdur-44v4

# SRT
ffmpeg -re -f lavfi -i testsrc2=rate=25:size=1280x720 -pix_fmt yuv420p -codec:v libx264 -b:v 2048k -preset:v ultrafast -f mpegts 'srt://localhost:8890?mode=listener&pkt_size=1316'

# SRT proper streamId 
ffmpeg -re -f lavfi -i testsrc2=rate=25:size=1280x720 -pix_fmt yuv420p -codec:v libx264 -b:v 2048k -preset:v ultrafast -f mpegts 'srt://example.com:8890?mode=caller&pkt_size=1316&streamid=publish:demo'
# Start stream


# Read stream
ffplay -i "rtmp://example.com:1935/live/demo"
ffplay -i "srt://localhost:8890?pkt_size=1316&mode=caller"
ffplay -i "srt://example.com:8890?streamid=read:demo&pkt_size=1316"

#http://192.168.1.10:8888/demo/
```

## Streaming Protokoller

- RTMP: Real-Time Messaging Protocol
- RTSP: Real-Time Streaming Protocol
- SRT: Secure Reliable Transport
- HLS: HTTP Live Streaming
- WebRTC: Web Real-Time Communication

### RTMP

RTMP (Real-Time Messaging Protocol) is a protocol primarily used to stream audio, video, and data over the internet in real time. If you're somewhat into streaming, you've probably encountered RTMP if you've used platforms like YouTube, Twitch, or Facebook Live.

Here’s a simplified breakdown of how it works:

1. **Purpose**: RTMP was originally developed by Adobe for their Flash Player, but it's still widely used today for live video streaming, especially in the first step of getting the video from a source (your camera) to a streaming server.

2. **How RTMP Works**:
   - **Ingest**: When you stream using a tool like OBS (Open Broadcaster Software), it encodes your video and sends it to a platform's server using RTMP.
   - **Delivery to Streaming Server**: RTMP breaks your stream into small packets of audio, video, and metadata, and sends them to the server. The "real-time" nature means there’s minimal delay in transmitting the data.
   - **Conversion for Viewers**: Once the platform receives the RTMP stream, it typically converts it to formats that are easier to distribute and play back, like HLS (HTTP Live Streaming) or DASH (Dynamic Adaptive Streaming over HTTP). This is necessary because RTMP itself isn't ideal for playback in modern web browsers.

3. **Why RTMP is Still Used**:
   - **Low Latency**: While not the absolute lowest latency available, RTMP still delivers a stream fast enough for many live events, keeping delays down to a few seconds.
   - **Ease of Use**: Many streaming software and hardware solutions still support RTMP, and it’s relatively simple to set up.
   - **Broad Platform Support**: Despite the decline of Flash, platforms like YouTube, Twitch, and others continue to use RTMP for ingesting live streams before transcoding them to formats more optimized for viewers.

4. **Drawbacks**:
   - **Not Browser-Friendly**: RTMP isn't natively supported by modern browsers anymore. That’s why platforms transcode the stream into something more compatible for viewers, like HLS.
   - **Higher Latency Compared to Newer Protocols**: Newer protocols (such as WebRTC) can offer lower latency, especially when ultra-low latency is needed.

In short, RTMP is how your streaming software sends your live stream to the server, but the server will usually convert that stream into something else that viewers can watch.

### RTSP

RTSP (Real-Time Streaming Protocol) is a different protocol from RTMP but is also used for streaming audio and video in real time. While RTMP is more commonly seen in live-streaming platforms (like Twitch or YouTube), RTSP is more often found in security cameras, surveillance systems, and professional video setups.

Here’s a breakdown of RTSP for someone familiar with streaming:

1. **Purpose**: RTSP is designed primarily for **controlling** the delivery of multimedia streams, rather than just streaming video directly. It works like a "remote control" that communicates with a media server. It allows you to play, pause, fast-forward, or rewind a stream. Think of RTSP as the protocol that manages the stream rather than just sending it.

2. **How RTSP Works**:
   - **Stream Control**: RTSP lets a client (e.g., a media player or a surveillance app) send commands to a streaming server, such as **PLAY**, **PAUSE**, **STOP**, or **RECORD**. It's like using a remote control to interact with the media.
   - **Delivery**: Unlike RTMP, RTSP usually works with other protocols to actually deliver the video or audio stream. It often uses **RTP (Real-Time Transport Protocol)** for sending the actual media content (audio and video packets).
   - **Live Streams**: For live-streaming scenarios (like security cameras), the client connects to a server using RTSP, and the server sends back the video stream using RTP or similar.

3. **Common Use Cases**:
   - **IP Cameras**: RTSP is extremely popular in the surveillance and security industry. Most IP cameras use RTSP to allow users to connect to them remotely and view live footage.
   - **Professional Broadcasting**: RTSP is sometimes used in professional broadcasting and media distribution, especially in systems where playback control is important.
   - **Media Servers**: Servers like VLC, Wowza, and others can use RTSP to control streams.

4. **Difference from RTMP**:
   - **Not Focused on Ingesting for the Web**: While RTMP is used for streaming to platforms like YouTube or Twitch, RTSP is typically used for controlling and managing streams from cameras or media servers. It’s not as common in traditional live streaming on the web.
   - **Stream Control**: RTSP allows clients to control the stream (play, pause, seek), which isn’t something RTMP does.
   - **Protocol Interaction**: RTSP works alongside other protocols like RTP and RTCP (Real-Time Control Protocol), whereas RTMP bundles everything (audio, video, metadata) in one protocol.

5. **Drawbacks**:
   - **Less Web Support**: Like RTMP, RTSP isn’t natively supported in most modern web browsers. You need specific players (e.g., VLC or custom software) to view an RTSP stream.
   - **More Complex Setup**: RTSP requires handling multiple protocols (RTP, RTCP) for the full streaming experience, making it a bit more complex than protocols like RTMP or HLS.

6. **Why Use RTSP?**:
   - **Direct Camera Feeds**: If you’re working with security cameras or live monitoring systems, RTSP is one of the main ways to get live video feeds.
   - **Precise Control**: It’s great for situations where you need to control the stream, like pausing or seeking during playback.

In summary, RTSP is often used in scenarios where you need to control the stream (like in surveillance systems), and it works with other protocols to deliver the actual video content. It's less about broadcasting to a large audience like RTMP, and more about direct control and access to live or on-demand media streams.

### SRT

Haivision SRT (Secure Reliable Transport) is a streaming protocol designed to improve the reliability and security of live video streams over unpredictable networks like the internet. It's especially useful for broadcasters, streaming platforms, and enterprises that need to deliver high-quality, low-latency video across long distances or through challenging network conditions (e.g., high packet loss, jitter, or fluctuating bandwidth).

Here’s a breakdown for someone familiar with streaming:

1. **Purpose**: 
   - SRT was created to enable secure, reliable, and low-latency video streaming over unstable networks (like the public internet), which are prone to packet loss, jitter, and fluctuating speeds. 
   - It’s ideal for streaming live video over long distances, where traditional streaming protocols might struggle with stability or quality.

2. **How SRT Works**:
   - **Error Correction**: SRT uses a technique called **ARQ (Automatic Repeat reQuest)**, where it automatically detects missing packets and requests them to be resent, ensuring minimal video or audio loss. This makes it more reliable over poor network conditions compared to RTMP or even RTSP.
   - **Low Latency**: SRT optimizes latency by dynamically adjusting for network conditions in real-time, so even if there’s packet loss or jitter, it can minimize delays while maintaining video quality.
   - **Secure Streaming**: It incorporates **AES encryption** to ensure that streams are secure, protecting the content from eavesdropping or interception, which is especially important in professional broadcasting or corporate environments.
   - **Bandwidth Optimization**: SRT adjusts its bitrate based on network conditions, allowing you to stream high-quality video even when the available bandwidth fluctuates.

3. **Key Use Cases**:
   - **Broadcasting**: Many broadcasters use SRT to stream high-quality video content from remote locations to their main servers or from live events. SRT ensures that even with inconsistent internet, they get a stable and clear stream.
   - **Live Streaming**: For live event producers, SRT can help deliver a more consistent stream when sending video to platforms, CDNs, or across long distances.
   - **Corporate Streaming**: Companies may use SRT for internal video communication, ensuring high-quality and secure video for global meetings or live broadcasts.
   - **Video Contribution and Distribution**: SRT is used in professional workflows where content needs to be sent reliably between locations or distributed across networks to multiple end-users.

4. **Comparison to RTMP, RTSP, and Other Protocols**:
   - **Compared to RTMP**: RTMP is widely used for live streaming but has limitations with network reliability, especially over long distances. SRT’s error correction and ability to handle network fluctuations make it more robust in poor conditions.
   - **Compared to RTSP**: RTSP is more about controlling streams from devices like cameras, while SRT is about reliably delivering high-quality streams over the internet. SRT excels in error correction and low-latency transmission, which RTSP doesn’t address.
   - **Latency**: SRT offers much lower latency than protocols like RTMP, which makes it more suitable for live broadcasting. It dynamically adjusts latency based on the network, minimizing delays without sacrificing video quality.

5. **Why SRT is Important**:
   - **Reliability in Poor Network Conditions**: SRT is designed to handle packet loss, jitter, and other network problems that would cause significant disruptions in other protocols.
   - **Low-Latency**: For live video, minimizing latency is crucial, and SRT is one of the best protocols for ensuring smooth, real-time streaming with minimal delay.
   - **Security**: The built-in encryption is critical for industries where content protection is essential (e.g., broadcasting, live sports, corporate streams).
   - **Open Source**: Unlike proprietary solutions, SRT is open-source, which means it's freely available to everyone and widely supported across platforms and devices.

6. **Drawbacks**:
   - **Not Universally Supported**: While SRT adoption is growing, it’s not yet as widely supported as RTMP, especially on consumer-facing platforms like Twitch or YouTube. You’ll more often see SRT used in professional settings.
   - **More Technical Complexity**: While powerful, setting up SRT streams can be more complex compared to RTMP or HLS. You need to ensure both your encoding and decoding systems support SRT.

In summary, Haivision SRT is a protocol designed for **secure, reliable, and low-latency streaming** over unreliable networks, making it ideal for professional broadcasters, live event producers, and enterprises. It’s more resilient to network issues than traditional protocols like RTMP or RTSP, making it a great choice for delivering high-quality live video when network conditions aren’t perfect.

### **HLS (HTTP Live Streaming)**

1. **Purpose**: 
   - HLS is a streaming protocol developed by Apple, primarily used to deliver video content over the internet. It's widely adopted for live streaming and video-on-demand (VOD) services and works well for large-scale distribution to many users.
   
2. **How HLS Works**:
   - **Segmenting the Stream**: HLS breaks video streams into small **chunks (usually 6-10 seconds each)** and sends them to users over HTTP. Each chunk is downloaded and played in sequence by the player.
   - **Playlist File (M3U8)**: HLS streams are accompanied by a playlist file (in `.m3u8` format), which tells the player where to find each chunk of the video. The player downloads the chunks one by one and plays them back in order.
   - **Adaptive Bitrate Streaming**: One of HLS’s strengths is that it supports adaptive bitrate streaming. This means that depending on the viewer's internet speed, the player can switch to higher or lower-quality chunks on the fly to ensure smooth playback.
   
3. **Strengths**:
   - **Scalability**: HLS is designed to scale really well. Since it uses standard HTTP servers (the same as web pages), it can easily handle millions of viewers.
   - **Compatibility**: HLS is supported across a wide range of devices, including mobile phones, smart TVs, desktops, and browsers (especially Safari). Almost all modern platforms can handle HLS.
   - **Adaptive Bitrate**: It provides a good experience even for users with slow or inconsistent internet, as it adjusts the stream quality to match their connection.
   
4. **Drawbacks**:
   - **Latency**: HLS typically has higher latency (15–30 seconds). This delay happens because the video is split into chunks and buffered by the player. While it's great for streaming VOD content or pre-recorded live streams, it’s not ideal for situations that demand real-time interaction (e.g., live sports commentary, video conferencing).
   - **Chunk Size**: The length of the video chunks can add to the delay. Even though newer versions of HLS can use smaller chunks (Low-Latency HLS), it’s still generally not as fast as some other protocols like WebRTC.

5. **Common Use Cases**:
   - **Video-on-Demand (VOD)**: Streaming platforms like Netflix or Hulu often use HLS because it delivers high-quality video at scale.
   - **Live Streaming**: Services like YouTube Live and some OTT platforms use HLS for live video streaming. It works well for large audiences, but there’s usually a noticeable delay.
   
---

### **WebRTC (Web Real-Time Communication)**

1. **Purpose**:
   - WebRTC is a protocol designed for **real-time communication**, like video conferencing, live chat, and peer-to-peer media sharing. It enables **very low-latency** video and audio streaming, typically used for one-to-one or small group interactions.
   
2. **How WebRTC Works**:
   - **Peer-to-Peer Communication**: Unlike HLS, which streams from a central server, WebRTC usually establishes a direct connection between peers (e.g., between two users). This allows for fast, low-latency communication.
   - **Real-Time Streaming**: WebRTC is optimized for real-time, interactive streaming, with delays as low as a few milliseconds. It uses technologies like **UDP (User Datagram Protocol)** and **SRTP (Secure Real-time Transport Protocol)** to transmit data efficiently, which makes it perfect for live, interactive applications.
   - **NAT Traversal and STUN/TURN Servers**: WebRTC has built-in mechanisms to handle connections between peers behind firewalls or NAT devices, making peer-to-peer communication possible even in restrictive network environments.
   
3. **Strengths**:
   - **Ultra-Low Latency**: The biggest strength of WebRTC is its near-instant communication. This makes it perfect for applications like video calls, live auctions, or real-time gaming, where even a one-second delay would be unacceptable.
   - **Browser Compatibility**: WebRTC is natively supported by modern web browsers (Chrome, Firefox, Safari, Edge), meaning users don’t need plugins or extra software for video conferencing or live, interactive video.
   - **Direct Peer-to-Peer Connections**: For small-scale or direct interactions (like video calls or live interviews), WebRTC allows two or more participants to connect directly, reducing server load and minimizing latency.

4. **Drawbacks**:
   - **Scalability**: Unlike HLS, WebRTC isn’t designed to stream to massive audiences. It’s perfect for real-time communication between a small number of users (like a few dozen in a video chat), but streaming to thousands or millions requires more complex infrastructure (e.g., using a media server to relay WebRTC streams).
   - **Complex Setup**: WebRTC is technically more complex to set up than HLS. It requires managing peer connections, handling NAT traversal, and securing streams, which adds complexity, especially for large deployments.
   - **No Built-in Adaptive Bitrate**: While WebRTC can adjust its bitrate based on the connection quality, it doesn’t have the same sophisticated adaptive bitrate streaming as HLS, where it dynamically switches between high and low-quality video chunks.

5. **Common Use Cases**:
   - **Video Conferencing**: Apps like Zoom, Google Meet, and Microsoft Teams leverage WebRTC to provide real-time video calls with minimal latency.
   - **Live Chat and Customer Support**: Many real-time chat and video support tools use WebRTC for instant communication.
   - **Real-Time Streaming for Gaming**: WebRTC can be used in multiplayer games or live game streaming, where low latency is crucial.

### **Comparison of HLS vs WebRTC**:

- **Latency**: 
  - **HLS**: Typically 10–30 seconds (higher for older HLS versions).
  - **WebRTC**: Real-time (sub-second delay).
  
- **Scalability**:
  - **HLS**: Highly scalable, capable of reaching millions of users via HTTP.
  - **WebRTC**: Limited scalability for direct peer-to-peer communication; requires media servers for larger groups.

- **Use Cases**:
  - **HLS**: Best for broadcasting live events, VOD, or streaming to large audiences with a slight delay.
  - **WebRTC**: Ideal for real-time communication like video calls, live customer support, or interactive live streaming.

- **Complexity**:
  - **HLS**: Easier to implement with existing infrastructure (uses HTTP servers).
  - **WebRTC**: More complex, especially for large-scale deployments (needs peer connection management, signaling, and possible use of STUN/TURN servers).

In summary, **HLS is great for large-scale video delivery** with slightly higher latency, while **WebRTC excels in real-time, low-latency interactions** where immediacy is critical, like video calls or live, interactive streams.


## Nettverk

![assets\tcp-udp-meme.png](assets\tcp-udp-meme.png)

When discussing streaming protocols like RTMP, RTSP, HLS, WebRTC, and SRT, it's essential to understand how **TCP (Transmission Control Protocol)** and **UDP (User Datagram Protocol)** influence how data is transmitted over the internet. These are the two primary transport protocols that determine how data packets are sent and received, each with its pros and cons for streaming.

### **TCP (Transmission Control Protocol)**

1. **What is TCP?**
   - TCP is a connection-oriented protocol, meaning it establishes a reliable connection between two devices before transmitting data. It ensures that every packet of data sent arrives at the destination in the correct order and without errors.
   - If packets are lost or arrive out of order, TCP will request that the data be retransmitted, ensuring perfect accuracy but at the cost of speed and higher latency.

2. **How TCP Works**:
   - **Handshake**: TCP starts by performing a three-way handshake to establish a connection.
   - **Error Checking and Retransmission**: It continuously checks that the data arrives intact, and if it detects a missing or corrupted packet, it requests the sender to resend it.
   - **Flow Control**: TCP adjusts the rate at which data is sent based on network conditions, ensuring smooth transmission without overwhelming the network.

3. **Strengths for Streaming**:
   - **Reliability**: TCP guarantees that all data will arrive at the destination correctly. This makes it useful for scenarios where accuracy is more important than speed, such as file transfers, web page loading, or any situation where a perfect copy of the data is necessary.
   - **Orderly Delivery**: TCP ensures that all data is received in the correct order, making it reliable for non-time-sensitive data.

4. **Weaknesses for Streaming**:
   - **Higher Latency**: Because of the error-checking and retransmission process, TCP can introduce higher latency. For live streaming, this is problematic because real-time interaction is essential.
   - **Not Ideal for Live or Real-Time Streaming**: The retransmission of lost packets causes delays, which can result in buffering or lag in live streaming scenarios.

5. **Protocols Using TCP**:
   - **HLS**: HLS relies on HTTP, which in turn uses TCP. Since HLS is designed for reliability and adaptive bitrate streaming over large-scale networks, TCP's robustness is valuable. However, this also means that HLS typically has higher latency compared to real-time streaming protocols.
   - **RTMP**: While RTMP also uses TCP, it is better suited for live streaming than HLS, but still has higher latency than protocols using UDP.

### **UDP (User Datagram Protocol)**

1. **What is UDP?**
   - UDP is a connectionless protocol, meaning it sends data without establishing a dedicated connection or ensuring the data arrives at its destination. It does not guarantee packet delivery, order, or integrity, which means packets can be lost or arrive out of order.
   - However, UDP is much faster and has lower latency than TCP because it doesn’t spend time on retransmissions or error-checking.

2. **How UDP Works**:
   - **No Handshake**: UDP does not establish a connection before sending data. It just sends packets (called datagrams) without worrying if they arrive or if they’re received in the correct order.
   - **No Retransmission**: If a packet is lost, UDP does not attempt to resend it. This is a trade-off for speed and low latency.

3. **Strengths for Streaming**:
   - **Low Latency**: UDP is excellent for real-time applications where latency is more important than perfect data integrity. For example, in live video chats or gaming, you'd rather lose a few packets than deal with lag or delays.
   - **Efficient for Real-Time**: Because it doesn’t wait for acknowledgments or retransmit lost packets, UDP is much more efficient for live, real-time communication like video calls, live gaming, and ultra-low-latency streaming.

4. **Weaknesses for Streaming**:
   - **Unreliable Delivery**: UDP doesn’t ensure that all packets will arrive. For some types of streaming, especially video-on-demand, this could lead to quality issues (e.g., glitches or missing frames).
   - **No Flow Control**: Without flow control, it’s easier to overwhelm the network, potentially causing packet loss or jitter (inconsistent packet arrival times).

5. **Protocols Using UDP**:
   - **WebRTC**: WebRTC uses UDP because it prioritizes low latency for real-time communication (e.g., video conferencing). Since it’s real-time, slight packet loss is acceptable, but high latency would ruin the experience.
   - **SRT**: SRT (Secure Reliable Transport) also uses UDP but adds error correction and retransmission mechanisms on top of it to make streaming reliable while maintaining low latency. This makes SRT more robust in handling network issues while still benefiting from UDP’s low-latency nature.
   - **RTSP**: RTSP often uses UDP to send real-time video streams, especially for low-latency needs like IP cameras or live broadcasting. However, it can also use TCP in cases where reliability is more important than speed.

---

### **Comparison of TCP and UDP in Streaming**:

- **Reliability vs Speed**:
  - **TCP**: Prioritizes reliable delivery at the cost of speed, making it suitable for protocols like HLS where accuracy is essential but real-time performance is less critical.
  - **UDP**: Focuses on speed and low latency, ideal for live, interactive applications like WebRTC or SRT, where some packet loss is acceptable as long as the stream is fast and responsive.

- **Latency**:
  - **TCP**: Higher latency due to retransmission of lost packets and the establishment of a connection.
  - **UDP**: Lower latency because there’s no retransmission or connection overhead, making it ideal for real-time streaming.

- **Error Handling**:
  - **TCP**: Built-in error handling (acknowledgment and retransmission), which ensures data integrity but can introduce delays.
  - **UDP**: No error handling by default, so packet loss may occur, but streaming protocols built on UDP (like WebRTC and SRT) can add custom mechanisms for error correction to compensate.

---

### **How They Apply to the Mentioned Protocols**:

1. **HLS (TCP)**:
   - HLS uses TCP because it is more about **delivering reliable, high-quality streams**. Latency isn't the top priority, especially for video-on-demand and live streams where a 10-30 second delay is acceptable for the sake of stream stability.

2. **WebRTC (UDP)**:
   - WebRTC uses UDP because it needs **real-time, ultra-low latency communication**. Slight packet loss is fine if it means the communication (e.g., video calls or live gaming) happens in real time without significant delays.

3. **RTMP (TCP)**:
   - RTMP uses TCP, ensuring the **reliable transmission of live streams**, but with slightly higher latency than WebRTC. It’s good for broadcasting to platforms like YouTube or Facebook, but not ideal for ultra-low-latency applications.

4. **SRT (UDP)**:
   - SRT uses UDP, but enhances it with **error correction** and retransmission to balance **low latency and reliability**. It's a middle ground between TCP’s reliability and UDP’s speed, making it ideal for professional live streaming.

5. **RTSP (UDP or TCP)**:
   - RTSP often uses UDP for **low-latency video streaming**, especially from IP cameras or live feeds. However, in some cases, it can switch to TCP for more reliable transmission if needed.

---

### **Summary**:

- **TCP** is about **reliability and ensuring all data is received correctly**, which is why it's used in protocols like HLS and RTMP where video quality is crucial, but it comes at the cost of higher latency.
- **UDP** is about **speed and low latency**, making it ideal for protocols like WebRTC and SRT where real-time performance is more important, even if some data gets lost.

## Kodek

![assets\H.264-vs-HEVC.png](assets\H.264-vs-HEVC.png)

https://www.epiphan.com/blog/h264-vs-h265/

**H.264** and **H.265 (also known as HEVC – High-Efficiency Video Coding)** are video compression standards that reduce the size of video files while maintaining quality. These codecs are essential for streaming, broadcasting, and storing video because they make it possible to deliver high-quality content efficiently over networks. Let's break down the key differences between the two and their role in video streaming.

### **H.264 (Advanced Video Coding or AVC)**

1. **What is H.264?**
   - H.264 is one of the most widely used video compression standards today. It was developed to deliver high-quality video at lower bitrates, making it a great balance between quality and file size.
   - It’s the backbone of most current video streaming services like YouTube, Netflix, and other platforms. Almost all devices, browsers, and media players support H.264 natively.

2. **How H.264 Works**:
   - **Intra-Frame Compression**: H.264 compresses video by reducing redundancy within individual frames.
   - **Inter-Frame Compression**: It also reduces redundancy between frames by predicting motion or changes between successive frames (known as temporal compression). This is key to reducing file sizes without losing too much quality.
   - **Bitrate Control**: H.264 can encode video using different bitrates (constant or variable), allowing flexibility in managing video quality based on available bandwidth.

3. **Strengths**:
   - **Compatibility**: H.264 is supported across virtually all platforms, devices, and browsers, making it a universal standard for video compression.
   - **Efficiency**: It provides good video quality with moderate file sizes and is efficient enough for most HD and even 4K content without requiring excessive computational power.
   - **Low Latency**: In live streaming or video conferencing scenarios, H.264’s low latency makes it a great option for real-time video applications.

4. **Weaknesses**:
   - **Not as Efficient as H.265**: While H.264 is highly efficient, it doesn’t offer the same compression efficiency as newer standards like H.265, especially for higher resolutions like 4K or 8K. Larger files are required to maintain high-quality video.
   - **Outdated for 4K/8K**: As we move into an era of ultra-high-definition video (4K/8K), H.264 can become too bandwidth-heavy compared to more advanced codecs like H.265.

5. **Common Use Cases**:
   - **Streaming Services**: YouTube, Netflix, Twitch, and many others rely heavily on H.264 to deliver HD content.
   - **Video Conferencing**: Platforms like Zoom, Google Meet, and Skype often use H.264 for real-time video transmission due to its low latency and wide support.
   - **Broadcasting and Blu-ray**: H.264 is also used in Blu-ray discs and traditional broadcast television.

### **H.265 (HEVC – High-Efficiency Video Coding)**

1. **What is H.265/HEVC?**
   - H.265, also known as HEVC (High-Efficiency Video Coding), is the successor to H.264. It offers significantly better compression efficiency, meaning it can deliver the same video quality as H.264 at roughly **half the bitrate**, or higher quality at the same bitrate.
   - H.265 is designed to handle high-resolution content, such as **4K and 8K**, more efficiently, making it increasingly important as demand for higher-quality video grows.

2. **How H.265 Works**:
   - **More Efficient Compression**: H.265 uses more advanced techniques for intra-frame and inter-frame compression, which significantly reduces the size of video files while maintaining or even improving video quality.
   - **Larger Block Sizes**: H.265 uses larger macroblocks (or "Coding Tree Units") up to 64x64 pixels, compared to H.264’s 16x16 pixels. This allows it to better compress high-resolution video, where fewer macroblocks can represent larger areas of static background.
   - **Better Motion Compensation**: H.265 improves on motion compensation techniques, resulting in more efficient prediction between frames, which is crucial for compressing fast-moving content like sports or action scenes.

3. **Strengths**:
   - **Superior Compression**: H.265 can achieve the same quality as H.264 at half the bitrate, or significantly better quality at the same bitrate. This makes it much more efficient for streaming high-quality video, especially in 4K and 8K resolutions.
   - **Bandwidth Savings**: H.265 reduces bandwidth requirements for streaming, which is crucial for delivering high-definition video over constrained networks or for users with limited internet speeds.
   - **Future-Proof**: With its ability to efficiently handle 4K, 8K, and beyond, H.265 is well-suited for the future of video streaming, particularly as more content shifts to ultra-high-definition.

4. **Weaknesses**:
   - **Computational Complexity**: H.265’s advanced compression techniques require more processing power to encode and decode video. This means that devices need more powerful hardware or software to handle H.265 compared to H.264.
   - **Licensing and Patent Issues**: H.265 is subject to more complex licensing and patent restrictions, which can make it more expensive for companies to implement than H.264. This has slowed its widespread adoption in some cases.
   - **Limited Support**: While H.265 is becoming more common, it’s not as universally supported as H.264. Older devices or software may not be able to decode H.265 without additional support or updates.

5. **Common Use Cases**:
   - **4K/8K Streaming**: Platforms like Netflix, Amazon Prime, and Apple TV are starting to use H.265 for streaming ultra-high-definition (UHD) content to save bandwidth while delivering pristine video quality.
   - **Video Storage**: For video storage (like on Blu-ray UHD discs), H.265 is increasingly used due to its superior compression, allowing more content to fit on physical media without sacrificing quality.
   - **Live Broadcasting**: For live 4K/8K broadcasting, H.265 is crucial to ensure lower bandwidth usage while maintaining quality.

---

### **Comparison Between H.264 and H.265**

| **Aspect**               | **H.264 (AVC)**                   | **H.265 (HEVC)**                      |
|--------------------------|------------------------------------|---------------------------------------|
| **Compression Efficiency**| Good                              | Superior (about 50% better than H.264)|
| **Bitrate**               | Requires higher bitrates for quality | Same quality at half the bitrate      |
| **Resolution Support**    | Handles up to 4K reasonably        | Optimized for 4K, 8K, and beyond      |
| **File Size**             | Larger than H.265 at the same quality | Smaller file sizes with the same quality |
| **Latency**               | Low for real-time communication    | Higher, but can be optimized          |
| **Device/Software Support**| Almost universally supported       | Growing, but not as widely supported as H.264 |
| **Processing Power**      | Requires less processing power     | Requires more processing power for encoding/decoding |
| **Use Cases**             | HD/Full HD streaming, video conferencing | 4K/8K streaming, Blu-ray UHD, broadcast |

### **When to Use H.264 vs H.265**:

- **H.264**: Still the best option for standard HD and Full HD streaming, video conferencing, and cases where broad device compatibility is critical. It's easier on processing power, and since it's universally supported, you can be confident that your audience will be able to watch your content without issues.
  
- **H.265**: Ideal for 4K and 8K streaming, where file size and bandwidth are significant concerns. If you're delivering content to audiences with newer devices or need to store high-quality video efficiently, H.265 is a better choice. It's particularly useful for content distribution over constrained networks or high-quality video storage.

### **Future Trends**:
- **H.266 (VVC – Versatile Video Coding)**: H.266 is the next generation after H.265, promising even greater compression efficiency, particularly for 8K video and immersive formats like VR and 360-degree video. However, adoption will take time, and H.264 and H.265 will remain dominant for years.

In summary, **H.264** is the current standard for most streaming applications, offering a great balance of quality and compatibility. **H.265**, while more efficient, is mainly used for higher-resolution content like 4K and 8K, as it provides superior compression but requires more processing power and has some limitations in device support.

## Transcoding

**Transcoding** refers to the process of converting a video or audio file from one format to another, typically to achieve compatibility with different devices, reduce file size, or optimize for a specific use case. This involves **decoding** the original media (converting it back to raw data) and then **re-encoding** it in a different format, resolution, or bitrate. 

Transcoding is widely used in video streaming, where content needs to be delivered in multiple formats and resolutions to accommodate varying network conditions and device capabilities. **FFmpeg** is one of the most popular tools for transcoding due to its flexibility, open-source nature, and support for a wide range of formats.

### **Why Transcoding is Important**

1. **Compatibility**:
   - Different devices (smartphones, TVs, tablets) and software players support different codecs and formats. A file encoded in one format might not play on all devices. For example, an MKV file might not play on an older TV, but if it's transcoded to MP4, it might.
   
2. **File Size and Bandwidth**:
   - Transcoding can reduce the file size by adjusting the **bitrate** or using more efficient codecs (e.g., transcoding from H.264 to H.265). This is crucial for streaming platforms to reduce bandwidth consumption and storage costs.
   
3. **Adaptive Streaming**:
   - Services like **YouTube, Netflix, or Twitch** need to deliver video at different resolutions (e.g., 1080p, 720p, 480p) based on the viewer's internet speed and device. This requires transcoding the original high-quality video into multiple versions.
   
4. **Quality Optimization**:
   - Sometimes, the original file may be too large or use outdated codecs that aren't efficient for modern streaming or storage. Transcoding allows you to compress and optimize content for better performance without noticeable loss of quality (or adjusting quality as needed).

---

### **How Transcoding Works**

1. **Decode the Original File**: 
   - The transcoder decodes the original file into raw data, which strips away the compression. For example, an H.264-encoded video will be decoded to its raw, uncompressed video frames.

2. **Re-encode into a New Format**:
   - The raw video is re-encoded into the desired format (e.g., from H.264 to H.265) and with different settings like bitrate, resolution, or frame rate. This new encoding is done according to the specifications you need for the target device or platform.

---

### **FFmpeg for Transcoding**

**FFmpeg** is a powerful, command-line-based multimedia framework that can be used to **decode, encode, transcode, stream, and manipulate** video and audio files. It supports almost every format and codec, making it a go-to solution for transcoding.

Here’s a basic example of transcoding using FFmpeg:

#### **1. Transcoding to a Different Format**
If you have a video in `.mkv` format that you want to convert to `.mp4`, you can use FFmpeg like this:

```bash
ffmpeg -i input.mkv output.mp4
```

- `-i input.mkv`: Specifies the input file.
- `output.mp4`: Specifies the output file in MP4 format. FFmpeg automatically handles the transcoding by detecting the formats of the input and output files.

#### **2. Transcoding with Codec Conversion**
You can also specify which video and audio codecs to use. For example, to transcode a video from **H.264** to **H.265**, you would use:

```bash
ffmpeg -i input.mp4 -c:v libx265 -c:a aac output_h265.mp4
```

- `-c:v libx265`: Tells FFmpeg to use the **H.265** codec for video.
- `-c:a aac`: Tells FFmpeg to use the **AAC** codec for audio.

This will result in a video with much smaller file size than the original H.264 version but with the same or slightly better quality due to the more efficient compression of H.265.

#### **3. Transcoding to Different Resolutions**
You can also transcode the video to different resolutions, which is useful for adaptive streaming. For example, to scale down a video to **720p**:

```bash
ffmpeg -i input.mp4 -vf scale=1280:720 -c:a copy output_720p.mp4
```

- `-vf scale=1280:720`: Applies a video filter (`-vf`) that scales the video to a resolution of 1280x720.
- `-c:a copy`: Copies the original audio without re-encoding it (since audio doesn’t need to change).

#### **4. Bitrate Control for Streaming**
When transcoding for streaming, controlling the bitrate is crucial. You can reduce the bitrate to save bandwidth:

```bash
ffmpeg -i input.mp4 -b:v 1500k -c:a aac output_1500k.mp4
```

- `-b:v 1500k`: Sets the video bitrate to 1500 kbps, which reduces the file size and bandwidth usage.

#### **5. Creating Multiple Bitrate Versions (for Adaptive Streaming)**

To create multiple versions of a video for adaptive streaming (like **HLS**), you might generate several outputs with different bitrates and resolutions:

```bash
ffmpeg -i input.mp4 -map 0:v -map 0:a \
  -s:v:0 1280x720 -b:v:0 3000k \
  -s:v:1 854x480 -b:v:1 1500k \
  -s:v:2 640x360 -b:v:2 800k \
  output_%03d.mp4
```

- `-map 0:v -map 0:a`: Maps both video and audio streams to all output files.
- `-s:v:0 1280x720 -b:v:0 3000k`: First output is 720p resolution with a 3000 kbps bitrate.
- `-s:v:1 854x480 -b:v:1 1500k`: Second output is 480p resolution with a 1500 kbps bitrate.
- `output_%03d.mp4`: Creates different files with multiple bitrates that can be used in adaptive streaming systems (like HLS).

---

### **Common Use Cases for Transcoding**

1. **Video Streaming Services (YouTube, Netflix)**:
   - These services transcode videos uploaded by users into multiple formats and resolutions to ensure compatibility across different devices and provide adaptive streaming. When you upload a video in 4K, the platform transcodes it into different versions (1080p, 720p, etc.) so users with slower connections can stream a lower-resolution version.
   
2. **Live Streaming (Twitch, Facebook Live)**:
   - For live streaming, transcoding is essential to deliver the stream to viewers with varying bandwidths. A live feed is transcoded into multiple resolutions in real-time so that the viewer's device or connection quality dictates which version they see.

3. **Video Conferencing**:
   - Services like Zoom or Google Meet often transcode video feeds to reduce bandwidth usage while ensuring that the quality of the video remains adequate for a wide range of internet connections and devices.

4. **Video Archiving**:
   - Transcoding can be used to convert raw or high-bitrate video files into more storage-efficient formats for archiving, especially when managing large video libraries.

---

### **Benefits of Transcoding**

- **Reduced Bandwidth and Storage Requirements**: Transcoding can reduce the size of a video file by re-encoding it with a more efficient codec or lower bitrate, making it more bandwidth-friendly for streaming or easier to store.
- **Device Compatibility**: By converting video files to more widely supported formats or codecs, transcoding ensures that the media can be played on a wide range of devices (e.g., smartphones, smart TVs, computers).
- **Adaptive Streaming**: Transcoding is a key process for creating different versions of a video file for adaptive bitrate streaming, where the video quality adjusts in real-time based on a user's internet speed.

---

### **Challenges of Transcoding**

1. **Computational Resources**:
   - Transcoding, especially for high-resolution videos like 4K, requires a lot of computational power, particularly when dealing with real-time transcoding for live streams.

2. **Time-Consuming**:
   - Transcoding large or high-quality files can take significant time, especially if the process includes re-encoding into multiple formats or resolutions.

3. **Quality Loss**:
   - Each time you transcode, especially if the new format uses a lossy codec, some quality is sacrificed. Care must be taken when adjusting settings to minimize perceptual loss.

---

In summary, **transcoding** is a vital process in media distribution that ensures videos can be delivered in the right format, resolution, and bitrate for various platforms, devices, and network conditions. **FFmpeg** is a powerful tool that simplifies this process, offering flexible options for format conversion, compression, and optimization.


## Optimizing Video for Low Bandwidth Usage

When optimizing video for **low bandwidth usage**, it's important to understand how **resolution**, **framerate**, and **bitrate** affect both the quality of the video and the amount of data that needs to be transmitted. Adjusting these parameters appropriately helps deliver watchable video even in environments with constrained bandwidth.

---

### **Resolution**

**Resolution** refers to the number of pixels in each dimension that a video frame contains, often expressed as width x height (e.g., **1920x1080** for Full HD or **1280x720** for 720p). The higher the resolution, the more detail the video can capture, but this also increases the file size and the amount of bandwidth required for streaming.

#### **Common Video Resolutions**:
- **1080p (Full HD)**: 1920x1080 pixels
- **720p (HD)**: 1280x720 pixels
- **480p (SD)**: 854x480 pixels
- **360p**: 640x360 pixels
- **240p**: 426x240 pixels

#### **Optimization for Low Bandwidth**:
Lowering the resolution is one of the most effective ways to reduce bandwidth usage. For instance:
- **1080p** video requires significantly more data than **720p** or **480p**.
- Reducing resolution decreases the number of pixels that need to be transmitted per frame, which directly reduces file size and required bandwidth.

For low bandwidth environments, you might opt for **480p or 360p**, as they maintain reasonable quality on smaller screens while consuming much less data.

---

### **Framerate**

**Framerate** (frames per second or **fps**) is the number of individual frames (images) displayed per second in a video. Common framerates include **24 fps** (used in movies), **30 fps** (standard for TV), and **60 fps** (used in gaming or high-action videos). Higher framerates provide smoother motion but require more data.

#### **Common Framerates**:
- **24 fps**: Standard for films and cinematic content.
- **30 fps**: Standard for TV and online video.
- **60 fps**: Used for sports, gaming, and fast-paced content.

#### **Optimization for Low Bandwidth**:
- Reducing the framerate lowers the number of frames transmitted per second, reducing the amount of data sent. For instance, switching from **60 fps** to **30 fps** can nearly halve the data rate while maintaining smoothness for most types of content.
- For static or slow-moving content, lowering to **24 fps** or even lower can further save bandwidth with minimal impact on perceived video quality.

For lower bandwidth usage, **30 fps** or even **24 fps** is often sufficient for most content that doesn't involve rapid motion, such as talking head videos or presentations.

---

### **Bitrate**

**Bitrate** is the amount of data used to encode each second of video, typically measured in **kilobits per second (kbps)** or **megabits per second (Mbps)**. It determines the quality of both the video and audio. Higher bitrates allow more data to represent the video, leading to better quality, but they also require more bandwidth.

#### **Common Bitrates**:
- **1080p at 60 fps**: 5,000 – 10,000 kbps (5 – 10 Mbps)
- **720p at 30 fps**: 1,500 – 4,000 kbps (1.5 – 4 Mbps)
- **480p at 30 fps**: 500 – 1,500 kbps (0.5 – 1.5 Mbps)
- **360p at 30 fps**: 300 – 700 kbps (0.3 – 0.7 Mbps)

#### **Optimization for Low Bandwidth**:
- Reducing the bitrate directly reduces the amount of data transmitted. However, lowering it too much can introduce visible artifacts, such as pixelation or blurriness, especially during fast motion scenes.
- To maintain quality while reducing bitrate, modern codecs like **H.265 (HEVC)** or **VP9** can be used, as they offer better compression efficiency than older standards like **H.264**.

For low bandwidth usage, adjusting the bitrate in tandem with resolution and framerate is crucial. For example, **480p at 30 fps** with a bitrate of around **500 kbps** can provide acceptable quality while conserving bandwidth.

---

### **Optimizing Video for Low Bandwidth Usage**

To optimize video for low bandwidth environments, it's often necessary to balance resolution, framerate, and bitrate. Here's how you can approach it:

#### 1. **Lower the Resolution**:
   - Reducing from **1080p to 720p** or **480p** is the quickest way to save bandwidth. The video will have fewer pixels, but depending on the device (such as smartphones), the quality reduction may not be very noticeable.

#### 2. **Reduce the Framerate**:
   - Lowering the framerate from **60 fps to 30 fps** or **24 fps** can significantly reduce the data that needs to be streamed without major quality loss for most types of content. 
   - For fast-moving content (sports, gaming), reducing framerate too much may result in choppy video, but for slower or static scenes, this is a great way to save bandwidth.

#### 3. **Lower the Bitrate**:
   - Choosing an appropriate bitrate is essential to balancing quality and bandwidth usage. For example:
     - **720p at 30 fps**: Around **2,000 – 3,000 kbps** is often optimal.
     - **480p at 30 fps**: You can go as low as **500 – 1,000 kbps** without sacrificing too much quality.
   - Use more efficient codecs like **H.265 (HEVC)** or **VP9**, which can maintain good quality at lower bitrates compared to older codecs like **H.264**.

#### 4. **Use Variable Bitrate (VBR)**:
   - Instead of constant bitrate (CBR), using **variable bitrate (VBR)** allows the bitrate to adjust dynamically depending on the complexity of the scene. For example, static scenes use lower bitrates, while high-motion scenes get more bitrate. This helps reduce the overall bandwidth usage without sacrificing quality.

#### 5. **Compress the Audio**:
   - Although audio generally takes up much less bandwidth than video, it can still be optimized. Use efficient audio codecs like **AAC** and set the bitrate according to the content. For example, **64 – 128 kbps** for stereo audio is often sufficient.

---

### **Practical Example of Optimization Using FFmpeg**

Using **FFmpeg**, here's how you could optimize a video for low-bandwidth streaming:

#### **Reducing Resolution and Bitrate**:
Convert a high-definition video to **480p** with a lower bitrate:

```bash
ffmpeg -i input.mp4 -s 854x480 -b:v 800k -c:a aac -b:a 96k output_480p.mp4
```

- `-s 854x480`: Rescales the video to **480p** resolution.
- `-b:v 800k`: Sets the video bitrate to **800 kbps**.
- `-c:a aac -b:a 96k`: Compresses the audio using the **AAC** codec with a bitrate of **96 kbps**.

#### **Reducing Framerate**:
To reduce both the resolution and framerate (from 60 fps to 30 fps):

```bash
ffmpeg -i input.mp4 -s 854x480 -r 30 -b:v 800k -c:a aac -b:a 96k output_480p_30fps.mp4
```

- `-r 30`: Reduces the framerate to **30 fps**, saving bandwidth by transmitting fewer frames per second.

---

### **Summary of Optimization Strategies for Low Bandwidth**:

1. **Lower Resolution**: Move from **1080p** to **720p** or **480p** for reduced data transmission.
2. **Reduce Framerate**: Use **30 fps** or lower if smooth motion isn't critical.
3. **Lower Bitrate**: Set an appropriate bitrate based on resolution, framerate, and content type. For 480p, around **500 – 1,000 kbps** is a good range.
4. **Use Efficient Codecs**: Switch to **H.265** or **VP9** to maintain quality with lower bitrates.
5. **Adjust Audio Settings**: Compress audio with a codec like **AAC** and use lower bitrates (e.g., **96 – 128 kbps**).

By balancing resolution, framerate, and bitrate, you can significantly reduce bandwidth usage while maintaining an acceptable level of video quality.

### Hvordan regne ut båndbredde

Båndbredde = Framerate x Bitrate

| Oppløsning | Framerate | Bitrate |
|------------|-----------|---------|
| 256x144    | 1         | 6k      |
| 256x144    | 4         | 20k     |
| 512x228    | 1         | 20k     |
| 512x228    | 6         | 80k     |
| 512x228    | 12        | 125k    |
| 512x228    | 25        | 250k    |
| 1024x576   | 1         | 120k    |
| 1024x576   | 6         | 300k    |
| 1024x576   | 12        | 500k    |
| 1024x576   | 25        | 750k    |
| 1280x720   | 1         | 150k    |
| 1280x720   | 6         | 450k    |
| 1280x720   | 12        | 650k    |
| 1280x720   | 25        | 1400k   |
| 1920x1080  | 1         | 400k    |
| 1920x1080  | 6         | 1000k   |
| 1920x1080  | 12        | 1800k   |
| 1920x1080  | 25        | 3000k   |

bufsize = bitrate / framerate
keyframe = fremerate * seconds

``` bash
INPUT="https://polarislive-lh.akamaized.net/hls/live/2039440/fvn/hzDaPl9KkIbkcZFUvWFfg/master.m3u8"

# 256x144 @ 1 fps @ 6k
ffmpeg -i $INPUT -vf scale=256:144 -r 1 -b:v 6k -minrate 6k -maxrate 6k -bufsize 3k -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f flv rtmp://example.com:1935/live/demo_256x144_1fps_6k

ffmpeg -i $INPUT -vf scale=256:144 -r 1 -b:v 6k -minrate 6k -maxrate 6k -bufsize 3k -g 3 -crf 23 -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f mpegts "srt://example.com:8890?streamid=publish:demo_256x144_1fps_6k&pkt_size=1316"

# 256x144 @ 4 fps @ 20k
ffmpeg -i $INPUT -vf scale=256:144 -r 4 -b:v 20k -minrate 20k -maxrate 20k -bufsize 5k -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f flv rtmp://example.com:1935/live/demo_256x144_4fps_20k

# 512x228 @ 1 fps @ 20k
ffmpeg -i $INPUT -vf scale=512:228 -r 1 -b:v 20k -minrate 20k -maxrate 20k -bufsize 20k -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f flv rtmp://example.com:1935/live/demo_512x228_1fps_20k

# 512x228 @ 6 fps @ 80k
ffmpeg -i $INPUT -vf scale=512:228 -r 6 -b:v 80k -minrate 80k -maxrate 80k -bufsize 14k -g 30 -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f flv rtmp://example.com:1935/live/demo_512x228_6fps_80k

# 512x228 @ 12 fps @ 125k
ffmpeg -i $INPUT -vf scale=512:228 -r 12 -b:v 125k -minrate 125k -maxrate 125k -bufsize 10k -g 60 -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f flv rtmp://example.com:1935/live/demo_512x228_12fps_125k

# 512x228 @ 25 fps @ 250k
ffmpeg -i $INPUT -vf scale=512:228 -r 25 -b:v 250k -minrate 250k -maxrate 250k -bufsize 20k -g 175 -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f flv rtmp://example.com:1935/live/demo_512x228_25fps_250k

# 1024x576 @ 1 fps @ 120k
ffmpeg -i $INPUT -vf scale=1024:576 -r 1 -b:v 120k -minrate 120k -maxrate 120k -bufsize 60k -g 5 -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f flv rtmp://example.com:1935/live/demo_1024x576_1fps_120k

# 1024x576 @ 6 fps @ 300k
ffmpeg -i $INPUT -vf scale=1024:576 -r 6 -b:v 300k -minrate 300k -maxrate 300k -bufsize 50k -g 30 -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f flv rtmp://example.com:1935/live/demo_1024x576_6fps_300k

# 1024x576 @ 6 fps @ 300k - HVEC/SRT
ffmpeg -i $INPUT -vf scale=1024:576 -r 6 -b:v 300k -minrate 300k -maxrate 300k -bufsize 50k -g 30 -crf 23 -pix_fmt yuv420p -c:v libx265 -preset ultrafast -tune zerolatency -f mpegts "srt://example.com:8890?streamid=publish:demo_1024x576_6fps_300k&pkt_size=1316"

# 1024x576 @ 6 fps @ 300k - HVEC/WebRTC
ffmpeg -i $INPUT -vf scale=1024:576 -r 6 -b:v 300k -minrate 300k -maxrate 300k -bufsize 50k -g 30 -pix_fmt yuv420p -c:v libx265 -preset ultrafast -tune zerolatency -f whip http://example.com:8889/demo/publish
```

## Programmering

Bør kunne programmere litt for å anvende streaming i praksis. Kombinasjon as Docker og Python er bra. For eksempel:


``` python
# https://github.com/Eyevinn/toolbox/blob/master/python/rtmp2srt.py
import argparse
import subprocess
from os.path import basename
import re
import glob

parser = argparse.ArgumentParser(description='Receive RTMP and restream over multicast')
parser.add_argument('streamkey', help='RTMP stream key (path)')
parser.add_argument('address', help='SRT address (IP:PORT)')
parser.add_argument('--caller', dest='caller', action='store_true', help='SRT in caller mode (default listener)')
parser.add_argument('--with-debug', dest='debug', action='store_true')
args = parser.parse_args()

mode = '&mode=listener'
if args.caller:
  mode = ''

if args.streamkey:
  mode += '&passphrase=' + args.streamkey

ffmpeg = "ffmpeg -fflags +genpts -listen 1 -re -i rtmp://0.0.0.0/rtmp/%s -acodec copy -vcodec copy -strict -2 -y -f mpegts srt://%s?pkt_size=1316%s" % (args.streamkey, args.address, mode)

if args.debug:
  print "%s" % ffmpeg
  print ffmpeg.split()

p1 = subprocess.Popen(ffmpeg.split())
output,err = p1.communicate()
```

``` dockerfile
FROM python:3.9-slim-bookworm
RUN apt-get update && apt-get install -y -qq ffmpeg
COPY python/rtmp2srt.py /root/rtmp2srt.py
ENTRYPOINT ["/root/rtmp2srt.py"]
CMD []
```

``` bash
docker build -t rtmp2srt .
docker run -it --rm rtmp2srt rtmp://example.com:1935/live/demo srt://example.com:8890?streamid=publish:demo --caller
```

Fordelen med å kunne programmere inn ffmpeg i Python og docker er at feilhåndtering og logging kan gjøres på en enkel måte. Dersom stream faller ut kan en ny stream startes automatisk. Dette kan enten gjøres med en enkel `while`-loop i python eller en restart always i docker.

En annen fordel med docker er at det kan kjøres på en hvilken som helst maskin som støtter docker. Dette gjør det enkelt å flytte applikasjonen til en annen maskin.

## Inkludering av KI

Lag og aktiver python virtual environment i Windows: 
    
```pwsh
python -m venv venv
venv\Scripts\Activate.ps1
```

### You Only Look Once (YOLO)

YOLO er en algoritme for objektgjenkjenning. Den er rask og nøyaktig. YOLO er en av de mest brukte algoritmene for objektgjenkjenning. Den er enkel å bruke og har god ytelse.

## Git og Git bash

Git is a version control system (VCS) that allows saving and tracking changes to files over time without overwriting previous snapshots. It helps developers collaborate on projects together.

https://www.baeldung.com/ops/git-guide

## SSH

SSH (Secure Shell) is a cryptographic network protocol for operating network services securely over an unsecured network. It is widely used for secure remote access to servers and for secure file transfers.

https://georgelitos.com/post/ssh-cheatsheet

## MQTT

