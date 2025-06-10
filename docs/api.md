# 📢 API Reference: Transcription Backend

This document describes the REST API endpoints exposed by the transcription backend. All routes are prefixed with `/v1`.

---

## 📑 Table of Contents

- [Base URL](#-base-url)
- [GET `/health`](#️-get-health)
- [POST `/transcribe`](#-post-transcribe)

  - [🔎 Supported Providers](#-supported-providers)

- [✅ Future Ideas](#-future-ideas)

---

## Base URL

```
http://localhost:8000/api/v1
```

---

## GET `/health`

Simple health check to verify the API is online.

### Response Body (`200 OK`)

```json
{
  "status": "ok",
  "message": "Service is running"
}
```

### Response Body (500 Internal Server Error)

```json
{
  "status": "error",
  "message": "Something went wrong on our side. Please try again later."
}
```

### Possible Status Codes

- `200 OK` – Server is healthy
- `500 Internal Server Error` – Something critical failed (e.g., database or dependency error)

---

## POST `/transcribe`

Transcribes an audio file using the selected provider.

### Request Body

```json
{
  "audio_url": "https://example.com/audio.mp3",
  "provider": "whisper"
}
```

| Field       | Type   | Required | Description                                 |
| ----------- | ------ | -------- | ------------------------------------------- |
| `audio_url` | string | ✅ Yes   | Public URL pointing to an audio file        |
| `provider`  | string | ✅ Yes   | Name of the provider (`whisper`, `open_ai`) |

### Response Body (`200 OK`)

```json
{
  "transcription": "This is the transcribed text."
}
```

| Field           | Type   | Description                          |
| --------------- | ------ | ------------------------------------ |
| `transcription` | string | The text result of the transcription |

### Possible Status Codes

- `200 OK` – Success
- `400 Bad Request` – Invalid input (e.g., unsupported provider)
- `500 Internal Server Error` – Unexpected error during transcription

### 🔎 Supported Providers

| Provider ID | Type    | Description                |
| ----------- | ------- | -------------------------- |
| `whisper`   | Offline | Uses Whisper model locally |
| `open_ai`   | Online  | Uses OpenAI Whisper API    |

You can pass these provider IDs in the `provider` field of `/transcribe` requests.

---

## ✅ Future Ideas

- Add `/status/:id` for tracking async jobs
- Add `/history` for past transcription logs (if database is added)
- Add support for file upload (`multipart/form-data`) instead of just URL
